from extractors.Base import BaseExtractor
from resources.globals import Path, utils, urlparse, requests, mimetypes, config
from resources.exceptions import InvalidPassedParam
from core.wheels import metadata_wheel, additional_metadata_wheel

class url(BaseExtractor):
    name = 'url'
    category = 'base'
    params = {
        "path": {
            "desc_key": "extractor_key_desc_path_path",
            "type": "string",
            "maxlength": 3
        },
        "type": {
            "desc_key": "extractor_key_desc_path_text",
            "type": "array",
            "values": ["copy", "move", "link"]
        }
    }

    def execute(self, args):
        url = args.get('url')
        if url == None:
            raise AttributeError("URL was not passed")
        
        parsed_url = urlparse(url)
        file_name = url
        if url.find('/'):
            file_name = parsed_url.path.split('/')[-1].split('?')[0]
        
        file_name_splitted = file_name.split('.')
        file_name = file_name_splitted[0]
        ext = ''
        if len(file_name_splitted) > 1:
            ext = file_name_splitted[1]

        # making request
        full_file_name = ''
        response = requests.get(url, allow_redirects=True, headers={
            "User-Agent": config.get("net.useragent")
        })
        if response.status_code != 200:
            raise FileNotFoundError('File not found')
        
        if file_name == '':
            file_name = requests.utils.quote(parsed_url.hostname) + '.'
        
        content_type = None
        t_extension  = None
        if ext == '':
            content_type = response.headers.get('Content-Type', '').lower()
            t_extension = mimetypes.guess_extension(content_type)
            if t_extension:
                ext = t_extension[1:]
            else:
                ext = 'html'
        
        full_file_name = '.'.join([file_name, ext])
        save_path = Path(self.temp_dir + '\\' + full_file_name)

        out_file = open(save_path, 'wb')
        out_file.write(response.content)
        out_file.close()
        
        metadata_resp = metadata_wheel(input_file=str(save_path))
        output_metadata = {
            "int_q_url": str(url), 
            "int_q_mime": str(t_extension),
            "full_name": str(full_file_name),
            "metadata": utils.extract_metadata_to_dict(metadata_resp),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(save_path))

        return {
            'format': ext,
            'original_name': full_file_name,
            'filesize': save_path.stat().st_size,
            'source': "url:"+url,
            'json_info': output_metadata
        }
