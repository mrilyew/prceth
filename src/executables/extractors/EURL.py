from executables.extractors.Base import BaseExtractor
from resources.Globals import os, download_manager, Path, utils, urlparse, requests, mimetypes, config, file_manager, ExecuteResponse
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

    def passParams(self, args):
        self.passed_params["url"] = args.get("url")

        super().passParams(args)
        assert self.passed_params.get("url") != None and self.passed_params.get("url") != "", "url was not passed"
    
    async def run(self, args):
        __parsed_url = urlparse(self.passed_params.get("url"))
        file_output_name = self.passed_params.get("url")
        if self.passed_params.get("url").find('/'):
            file_output_name = __parsed_url.path.split('/')[-1].split('?')[0]
        
        file_output_name_split = file_output_name.split('.')

        file_output_name = file_output_name_split[0]
        file_output_ext = ''
        if len(file_output_name_split) > 1:
            file_output_ext = file_output_name_split[-1]

        # Making HTTP request
        final_file_name = '.'.join([file_output_name, file_output_ext])
        save_path = Path(os.path.join(self.temp_dir, final_file_name))

        HTTP_REQUEST = await download_manager.addDownload(end=self.passed_params.get("url"),dir=save_path)
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
        
        file_size = save_path.stat().st_size

        output_metadata = {
            "original_url": str(self.passed_params.get("url")), 
            "mime": str(MIME_EXT),
            "output_name": str(final_file_name),
            "metadata": utils.extract_metadata_to_dict(metadata_wheel(input_file=str(save_path))),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(save_path))

        return ExecuteResponse(
            format=file_output_ext,
            original_name=final_file_name,
            filesize=file_size,
            source="url:"+self.passed_params.get("url"),
            json_info=output_metadata
        )

    def describeSource(self, INPUT_ENTITY):
        return {"type": "url", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
