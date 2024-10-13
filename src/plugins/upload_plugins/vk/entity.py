from plugins.upload_plugins.vk.vk import base_vk
from resources.globals import json, requests, urlencode, utils, consts, ApiException

class entity(base_vk):
    name = 'vk.entity'
    works = 'all'
    category = 'vk'

    def run(self, args=None):
        self.check_args(args=args)
        self.id = args.get('id')
        self.buffer = self.id
        if self.id == None:
            if args.get('shortcode') == None:
                raise AttributeError("Id was not passed")
            else:
                self.buffer = args.get('shortcode')
                __shortcode = utils.fast_get_request(f'{self.vk_url}utils.resolveScreenName?screen_name={args.get('shortcode')}',user_agent=self.user_agent)
                __shortcode_data = __shortcode.get('response')
                self.id = int(__shortcode_data.get('object_id'))
                if __shortcode_data.get('object_id') != None:
                    self.id = abs(int(__shortcode_data.get('object_id')))
                
                if __shortcode_data.get('type') == 'group':
                    self.id *= -1
        else:
            if self.id.find('id'):
                self.id = int(self.id.replace('id', ''))
            elif self.id.find('club') or self.id.find('public') or self.id.find('group') or self.id.find('event'):
                self.id = abs(int(self.id.replace('club', '').replace('public', '').replace('group', '').replace('event', '')))
                self.id *= -1

        request_method = 'users.get'
        request_params = {'access_token': self.vk_token}
        if self.id < 0:
            request_method = 'groups.getById'
            request_params['group_ids'] = abs(self.id)
            request_params['fields'] = consts['vk.group_fields']
        else:
            request_params['user_ids'] = abs(self.id)
            request_params['fields'] = consts['vk.user_group_fields']
        
        request_params['v'] = consts['vk.version']

        __entity_info = utils.fast_get_request(url=f'{self.vk_url}{request_method}?{urlencode(request_params)}',user_agent=self.user_agent)
        __entity_info_data_response = __entity_info.get('response')
        if 'error' in __entity_info_data_response:
            raise ApiException(__entity_info.get('error'))
        
        entity_array = None
        if self.id < 0:
            entity_array = __entity_info_data_response.get('groups')
        else:
            entity_array = __entity_info_data_response

        if len(entity_array) < 1:
            raise ApiException('Not found')

        file_name = f'{self.id}.json'
        path      = self.temp_dir + '\\' + file_name
        filesize   = len(str(__entity_info_data_response).encode('utf-8'))
        item = entity_array[0]

        stream = open(path, 'w')
        stream.write(json.dumps(item))
        stream.close()

        cached_content = {
            'type': 'group' if self.id < 0 else 'user',
            'name': f'{item.get('first_name')} {item.get('last_name')}' if self.id < 0 else item.get('name'),
        }

        indexed_info = ''
        if self.id < 0:
            indexed_info = ''
        else:
            indexed_info = f'{item.get('first_name')} {item.get('last_name')}'

        return {
            'format': 'json',
            'original_name': file_name,
            'filesize': filesize,
            'source': f'{self.vk_web_url}{self.buffer}',
            'cached_content': cached_content,
            'indexed_info': indexed_info
        }
