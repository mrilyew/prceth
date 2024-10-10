from core.settings import settings
from resources.consts import consts
from core.utils import utils
from resources.exceptions import ApiException
from plugins.BasePlugins import BaseUploadPlugin
from urllib.parse import urlencode
import requests
import json

class post(BaseUploadPlugin):
    name = 'vk.post'
    works = 'all'
    category = 'vk'

    def run(self, args=None):
        # Args
        post_id = args.get('post')
        download_attachments = bool(args.get('attachments_download'))
        save_reactions = bool(args.get('save_reactions'))

        if post_id == None:
            raise AttributeError("Post was not passed")

        if post_id.find('wall') != -1:
            post_id = post_id.replace('wall', '')

        vk_token = args.get('vk_token')
        if vk_token == None:
            vk_token = settings.get('vk.access_token')

        if vk_token == None:
            raise AttributeError("Token was not passed")

        user_agent = args.get('user_agent')
        if user_agent == None:
            user_agent = consts.get('vk.cool_useragent')
        
        vk_url = args.get('vk_url')
        vk_web_url = args.get('vk_web_url')
        if vk_url == None:
            vk_url = 'https://api.vk.com/method/'

        if vk_web_url == None:
            vk_web_url = 'https://vk.com/'
        
        # Request params
        request_params = {'access_token': vk_token}
        request_params['posts'] = post_id
        request_params['v'] = '5.238'
        request_params['extended'] = 1
        request_params['fields'] = consts['vk.user_group_fields']
        
        # Making request
        request_path = f'{vk_url}wall.getById?{urlencode(request_params)}'
        response_res = requests.get(request_path, headers={
            'User-Agent': user_agent
        })

        print('Downloaded post')

        response_raw = response_res.content
        response_json = json.loads(response_raw)
        if 'error' in response_json:
            raise ApiException(response_json.get('error'))
        
        response = response_json.get('response')
        if len(response.get('items')) < 1:
            raise ApiException('Post not found')
        
        # Formating
        items = response.get('items')
        post = items[0]
        post.pop('track_code')
        file_name = f'{post.get('id')}.json'
        path = self.temp_dir + '\\' + file_name

        profiles = response.get('profiles')
        groups = response.get('groups')

        index_info = ''
        filesize = len(str(response_json).encode('utf-8'))

        def format_photo(photo_to_format, path_dir='', filesize=0):
            uid = f'{photo_to_format.get('owner_id')}_{photo_to_format.get('id')}'
            print(f'Photo {uid} downloaded')

            orig_photo = photo_to_format.get('orig_photo')
            if orig_photo != None:
                orig_photo_url = orig_photo.get('url')
                response_pic = requests.get(orig_photo_url, allow_redirects=True, headers={
                    'User-Agent': user_agent
                })

                filesize += len(response_pic.content)
                
                stream = open(str(path_dir) + f'\\photo{uid}.jpg', 'wb')
                stream.write(response_pic.content)
                stream.close()

                photo_to_format.get('orig_photo')['url'] = f'\\attachments\\photo{uid}.jpg'

            return photo_to_format
        
        def format_post(post_to_format, index_info='', filesize=0):
            '''
            if post_to_format.get('owner_id') != None:
                post_to_format['owner'] = utils.find_owner(post_to_format.get('owner_id'), profiles, groups)
            
            if post_to_format.get('from_id') != None:
                post_to_format['from'] = utils.find_owner(post_to_format.get('from_id'), profiles, groups)     
            
            if post_to_format.get('signer_id') != None:
                post_to_format['signer'] = utils.find_owner(post_to_format.get('signer_id'), profiles, groups)
            '''

            # todo кэширование списка плагинов и упрощение поиска
            
            post_text = post_to_format.get('text')
            if post_text == None:
                post_text = ''
            
            if download_attachments == True and post_to_format.get('attachments') != None and len(post_to_format.get('attachments')) > 0:
                i = 0
                attachment_path = utils.str_to_path(self.temp_dir + '\\attachments')
                attachment_path.mkdir(exist_ok=True)
                for attachment in post_to_format.get('attachments'):
                    attachment_type = attachment.get('type')
                    attachment_info = attachment.get(attachment_type)

                    match attachment_type:
                        case 'photo':
                            post_to_format.get('attachments')[i] = format_photo(photo_to_format=attachment_info,path_dir=attachment_path,filesize=filesize)
                    
                    i += 1
            
            index_info += f' {str(post_text)} '
            copy_history = post_to_format.get('copy_history')
            if copy_history != None and len(copy_history) > 0:
                leng = len(copy_history)
                for i in range(0, leng):
                    for copy in copy_history:
                        post_to_format.get('copy_history')[i] = format_post(copy, index_info=index_info, filesize=filesize)

            return post_to_format
        
        for profile in profiles:
            index_info += f' {profile.get('screen_name')} {profile.get('id')} {profile.get('first_name')} {profile.get('last_name')} '
        
        for group in groups:
            index_info += f' {group.get('screen_name')} {int(group.get('id')) * -1} {group.get('name')} '
        
        post = format_post(post_to_format=post, index_info=index_info, filesize=filesize)
        response_post = {
            'items': [post],
            'profiles': profiles,
            'groups': groups
        }

        if response.get('reaction_sets') != None and save_reactions == True:
            response_post['reaction_sets'] = response.get('reaction_sets')

        # Writing JSON
        stream = open(path, 'w', encoding='utf-8')
        stream.write(json.dumps(response_post))
        stream.close()

        # Making cached content
        views = post.get('views')
        
        cached_content = {
            'type': 'post',
            'text': post.get('text'),
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
            'source': f'{vk_web_url}wall{post_id}',
            'cached_content': cached_content,
            'index_info': index_info.replace('None', '').replace('  ', ' '),
        }
