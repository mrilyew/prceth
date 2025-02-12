from executables.extractors.Base import BaseExtractor
from resources.Globals import Path, utils, urlparse, requests, mimetypes, config, file_manager, ExecuteResponse
from resources.Exceptions import NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel

# Base URL downloader. Downloads single file, without styles, images or something.
class EURL(BaseExtractor):
    name = 'EURL'
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
        input_url = args.get("url", None)
        if input_url == None or input_url == "":
            raise NotPassedException("url was not passed")
        
        __parsed_url = urlparse(input_url)
        file_output_name = input_url
        if input_url.find('/'):
            file_output_name = __parsed_url.path.split('/')[-1].split('?')[0]
        
        file_output_name_split = file_output_name.split('.')

        file_output_name = file_output_name_split[0]
        file_output_ext = ''
        if len(file_output_name_split) > 1:
            file_output_ext = file_output_name_split[-1]

        # Making HTTP request
        # TODO rewrite to DownloadManager
        # TODO rewrite
        HTTP_REQUEST = requests.get(input_url, allow_redirects=True, headers={
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

        output_metadata = {
            "original_url": str(input_url), 
            "mime": str(MIME_EXT),
            "output_name": str(final_file_name),
            "metadata": utils.extract_metadata_to_dict(metadata_wheel(input_file=str(save_path))),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(save_path))

        return ExecuteResponse(
            format=file_output_ext,
            original_name=final_file_name,
            filesize=file_size,
            source="url:"+input_url,
            json_info=output_metadata
        )
