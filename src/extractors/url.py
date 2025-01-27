from extractors.Base import BaseExtractor
from resources.globals import Path, utils, urlparse, requests, mimetypes, config, file_manager
from resources.exceptions import NotPassedException
from core.wheels import metadata_wheel, additional_metadata_wheel

# Base URL downloader. Downloads single file, without styles, images or something.
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
        # Getting params
        url = args.get('url')
        if url == None or url == "":
            raise NotPassedException("URL was not passed")
        __parsed_url = urlparse(url)
        file_output_name = url
        if url.find('/'):
            file_output_name = __parsed_url.path.split('/')[-1].split('?')[0]
        
        file_splitted_array = file_output_name.split('.')
        file_output_name = file_splitted_array[0]
        file_output_ext = ''
        if len(file_splitted_array) > 1:
            file_output_ext = file_splitted_array[-1]

        # making request
        HTTP_REQUEST = requests.get(url, allow_redirects=True, headers={
            "User-Agent": config.get("net.useragent")
        })
        HTTP_REQUEST_STATUS = HTTP_REQUEST.status_code
        if HTTP_REQUEST_STATUS == 404 or HTTP_REQUEST_STATUS == 403:
            raise FileNotFoundError('File not found')
        if file_output_name == '':
            file_output_name = requests.utils.quote(__parsed_url.hostname) + '.'
        
        CONTENT_TYPE = HTTP_REQUEST.headers.get('Content-Type', '').lower()
        MIME_EXT     = None
        if file_output_ext == '' or utils.is_generated_ext(file_output_ext):
            CONTENT_TYPE = CONTENT_TYPE
            MIME_EXT = mimetypes.guess_extension(CONTENT_TYPE)
            if MIME_EXT:
                file_output_ext = MIME_EXT[1:]
            else:
                file_output_ext = 'html'
        
        final_file_name = '.'.join([file_output_name, file_output_ext])
        save_path = Path(self.temp_dir + '\\' + final_file_name)
        file_manager.newFile(path=save_path, content=HTTP_REQUEST.content)
        file_size = save_path.stat().st_size
        
        metadata_resp = metadata_wheel(input_file=str(save_path))
        output_metadata = {
            "int_q_url": str(url), 
            "int_q_mime": str(MIME_EXT),
            "full_name": str(final_file_name),
            "metadata": utils.extract_metadata_to_dict(metadata_resp),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(save_path))

        return {
            'format': file_output_ext,
            'original_name': final_file_name,
            'filesize': file_size,
            'source': "url:"+url,
            'json_info': output_metadata
        }
