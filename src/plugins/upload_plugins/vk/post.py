from core.settings import settings
from resources.consts import consts
from core.utils import utils
from resources.exceptions import ApiException
from plugins.upload_plugins.vk.vk import base_vk
from plugins.upload_plugins.vk.photo import photo
from urllib.parse import urlencode
import requests
import json

class post(base_vk):
    name = 'vk.post'
    works = 'all'
    category = 'vk'
    short_name = 'wall'

    def run(self, args=None):
        # Args
        self.check_args(args=args)
        attachments_download = bool(args.get('attachments_download') or 0)
        save_reactions = bool(args.get('save_reactions'))

        # Request params
        request_params = {'access_token': self.vk_token}
        request_params['posts'] = self.id
        request_params['v'] = consts['vk.version']
        request_params['extended'] = 1
        request_params['fields'] = consts['vk.user_group_fields']
        
        # Making request
        api_post = requests.get(f'{self.vk_url}wall.getById?{urlencode(request_params)}', headers={
            'User-Agent': self.user_agent
        })

        print('Recieved post api info')

        __response_raw = api_post.content
        __response_json = json.loads(__response_raw)
        if 'error' in __response_json:
            raise ApiException(__response_json.get('error'))
        
        # Consts
        __response = __response_json.get('response')
        items     = __response.get('items')
        post      = items[0]
        post.pop('track_code')
        file_name = f'{post.get('id')}.json'
        path      = self.temp_dir + '\\' + file_name
        profiles  = __response.get('profiles')
        groups    = __response.get('groups')
        if len(items) < 1:
            raise ApiException('Post not found')

        views = post.get('views')

        index_info = ''
        filesize = len(str(__response_json).encode('utf-8'))
        
        def __format_post(arg_post, index_info='', filesize=0):
            # todo кэширование списка плагинов и упрощение поиска
            post_text         = arg_post.get('text')
            post_attachments  = arg_post.get('attachments')
            post_copy_history = arg_post.get('copy_history')
            post_copy_length  = len(post_copy_history or [])
            if post_text == None:
                post_text = ''

            post_text = post_text.strip()
            
            if attachments_download == True and post_attachments != None and len(post_attachments) > 0:
                i = 0
                attachments_path = utils.str_to_path(self.temp_dir + '\\attachments')
                attachments_path.mkdir(exist_ok=True)

                for attachment in post_attachments:
                    attachment_type = attachment.get('type')
                    attachment_info = attachment.get(attachment_type)
                    attachment_id   = f'{attachment_info.get('owner_id')}_{attachment_info.get('id')}'
                    attachment_path = utils.str_to_path(self.temp_dir + f'\\attachments\\{attachment_type}{attachment_id}')
                    attachment_path.mkdir(exist_ok=True)

                    match attachment_type:
                        case 'photo':
                            photo_plugin = photo(temp_dir=str(attachment_path))
                            res = photo_plugin.run(args={'id':attachment_id,'photo_pre':attachment_info})
                            post_attachments[i] = res.get('item')
                    
                    i += 1
            
            index_info += f' {str(post_text)} '
            
            if post_copy_history != None and post_copy_length > 0:
                for i in range(0, post_copy_length):
                    for copy in post_copy_history:
                        arg_post.get('copy_history')[i] = __format_post(arg_post=copy, index_info=index_info, filesize=filesize)

            return arg_post
        
        for profile in profiles:
            index_info += f' {profile.get('screen_name')} {profile.get('id')} {profile.get('first_name')} {profile.get('last_name')} '
        
        for group in groups:
            index_info += f' {group.get('screen_name')} {int(group.get('id')) * -1} {group.get('name')} '
        
        post = __format_post(arg_post=post, index_info=index_info, filesize=filesize)
        response_post = {
            'items': [post],
            'profiles': profiles,
            'groups': groups
        }

        if __response.get('reaction_sets') != None and save_reactions == True:
            response_post['reaction_sets'] = __response.get('reaction_sets')

        # Writing post JSON
        stream = open(path, 'w', encoding='utf-8')
        stream.write(json.dumps(response_post))
        stream.close()

        # Making cached content
        
        cached_content = {
            'type': 'post',
            'from_id': post.get('from_id'),
            'owner_id': post.get('owner_id'),
            'date': post.get('date'),
        }

        if views != None:
            cached_content['views'] = views.get('count')
        
        return {
            'format': 'json',
            'original_name': file_name,
            'filesize': filesize,
            'source': f'{self.vk_web_url}wall{self.id}',
            'cached_content': cached_content,
            'index_info': index_info,
        }
