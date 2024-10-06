from core.settings import settings
from resources.consts import consts
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
        post_id = args.get('post')
        download_attachments = args.get('attachments_download')

        if post_id == None:
            raise AttributeError("Post was not passed")

        vk_token = args.get('vk_token')
        if vk_token == None:
            vk_token = settings.get('vk.access_token')

        if vk_token == None:
            raise AttributeError("Token was not passed")
        
        vk_url = args.get('vk_url')
        if vk_url == None:
            vk_url = 'https://api.vk.com/method/'
        
        request_params = {'access_token': vk_token}
        request_params['posts'] = post_id
        request_params['v'] = '5.238'
        request_params['extended'] = 1
        request_params['fields'] = consts['vk.user_group_fields']

        request_path = f'{vk_url}wall.getById?{urlencode(request_params)}'
        response_res = requests.get(request_path)
        response_raw = response_res.content
        response_json = json.loads(response_raw)
        if 'error' in response_json:
            raise ApiException('Post not found')
        
        response = response_json.get('response')
        if len(response.get('items')) < 1:
            raise ApiException('Post not found')
        
        items = response.get('items')
        post = items[0]
        file_name = f'{post.get('id')}.json'
        path = self.temp_dir + '\\' + file_name

        stream = open(path, 'w', encoding='utf-8')
        stream.write(json.dumps(response))
        stream.close()

        return {
            'format': 'json',
            'original_name': file_name,
            'filesize': response_raw.__sizeof__(),
            'source': f'https://vk.com/wall{post_id}'
        }
