from plugins.upload_plugins.vk.vk import base_vk
from resources.globals import json, requests, urlencode, utils, consts, ApiException

class photo(base_vk):
    name = 'vk.photo'
    works = 'all'
    category = 'vk'
    short_name = 'photo'

    def run(self, args=None):
        self.check_args(args=args)
        save_attachment_photo_sizes = int(args.get('save_attachment_photo_sizes') or 0) == 1
        sizes_path  = args.get('sizes_path') or 'sizes'

        # Request params
        request_params = {'access_token': self.vk_token}
        request_params['photos'] = self.id
        request_params['v'] = consts['vk.version']
        request_params['extended'] = 1
        request_params['photo_sizes'] = 1

        # Making request
        api_photo = None
        __response_json = None
        if args.get('photo_pre') != None:
            api_photo = args.get('photo_pre')
            __response_json = {"response": [api_photo]}
        else:
            request_path = f'{self.vk_url}photos.getById?{urlencode(request_params)}'
            api_photo = requests.get(request_path, headers={
                'User-Agent': self.user_agent
            })
            __response_json = json.loads(api_photo.content)
        
        if 'error' in __response_json:
            raise ApiException(__response_json.get('error'))
        
        print(f'Recieved photo{self.id} info')

        # Consts
        response = __response_json.get('response')
        item = response[0]
        if len(response) < 1:
            raise ApiException('Item not found')
        
        uid        = f'{item.get('owner_id')}_{item.get('id')}'
        file_name  = f'photo{uid}.json'
        path       = self.temp_dir + '\\' + file_name
        filesize   = len(str(__response_json).encode('utf-8'))
        index_info = f'{item.get('owner_id')}_{item.get('id')} {item.get('owner_id')} {item.get('id')} {item.get('text')}'
        
        orig_photo = item.get('orig_photo')

        # Saving original photo
        if orig_photo != None:
            orig_photo_url = orig_photo.get('url')
            response_pic = requests.get(orig_photo_url, allow_redirects=True, headers={
                'User-Agent': self.user_agent
            })

            filesize += len(response_pic.content)
            
            stream = open(f'{self.temp_dir}\\photo{uid}.jpg', 'wb')
            stream.write(response_pic.content)
            stream.close()

            item.get('orig_photo')['original_url'] = item.get('orig_photo')['url']
            item.get('orig_photo')['url'] = f'photo{uid}.jpg'
        else:
            save_attachment_photo_sizes = True

        sizes = sorted(item.get('sizes'), key=lambda size: size['height'], reverse=True)
        # Saving all sizes if need
        if save_attachment_photo_sizes == True:
            sizes_path_full   = utils.str_to_path(f'{self.temp_dir}\\{sizes_path}')
            sizes_path_full.mkdir(exist_ok=True)
            for size in sizes:
                response_pic = requests.get(size.get('url'), allow_redirects=True, headers={
                    'User-Agent': self.user_agent
                })

                filesize += len(response_pic.content)
                size_name = f'photo{uid}_{size.get('type')}'
                size_path = f'{sizes_path_full}\\{size_name}.jpg'

                print(f'Downloaded size {size.get('type')} {size.get('width')}x{size.get('height')}')

                size['original_url'] = size.get('url')
                size['url'] = f'{sizes_path}\\{size_name}.jpg'

                # Saving file
                stream = open(size_path, 'wb')
                stream.write(response_pic.content)
                stream.close()

        # Writing API photo
        stream = open(path, 'w', encoding='utf-8')
        stream.write(json.dumps(item))
        stream.close()

        return {
            'format': 'json',
            'original_name': file_name,
            'filesize': filesize,
            'cached_content': {
                'type': 'photo',
                'date': item.get('date'),
            },
            'index_info': index_info,
            'source': f'{self.vk_web_url}photo{self.id}',
            'item': item,
        }
