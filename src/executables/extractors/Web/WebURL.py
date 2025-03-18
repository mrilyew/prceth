from executables.extractors.Base import BaseExtractor
from resources.Globals import os, download_manager, Path, utils, requests, mimetypes, config, file_manager
from resources.Exceptions import NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel
from db.File import File

# Base URL downloader. Downloads single file, without styles, images or something.
class WebURL(BaseExtractor):
    name = 'WebURL'
    category = 'Web'
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

    def setArgs(self, args):
        self.passed_params["url"] = args.get("url")

        super().setArgs(args)
        assert self.passed_params.get("url") != None and self.passed_params.get("url") != "", "url was not passed"
    
    async def run(self, args = {}):
        PASSED_URL = self.passed_params.get("url")
        name, ext = utils.nameFromURL(PASSED_URL)

        # Making HTTP request
        JOINED_FILE_NAME = '.'.join([name, ext])
        save_path = Path(os.path.join(self.temp_dir, JOINED_FILE_NAME))

        HTTP_REQUEST = await download_manager.addDownload(end=self.passed_params.get("url"),dir=save_path)
        
        CONTENT_TYPE = HTTP_REQUEST.headers.get('Content-Type', '').lower()
        MIME_EXT     = None
        if ext == '' or utils.is_generated_ext(ext):
            CONTENT_TYPE = CONTENT_TYPE
            MIME_EXT = mimetypes.guess_extension(CONTENT_TYPE)
            if MIME_EXT:
                ext = MIME_EXT[1:]
            else:
                ext = 'html'
        
        file_size = save_path.stat().st_size

        output_metadata = {
            "original_url": str(self.passed_params.get("url")), 
            "mime": str(MIME_EXT),
            "output_name": str(JOINED_FILE_NAME),
            "metadata": utils.extract_metadata_to_dict(metadata_wheel(input_file=str(save_path))),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(save_path))
        FILE = self._fileFromJson({
            "extension": ext,
            "upload_name": JOINED_FILE_NAME,
            "filesize": file_size,
        })
        ENTITY = self._entityFromJson({
            "file": FILE,
            "source": "url:"+self.passed_params.get("url"),
            "entity_internal_content": output_metadata,
            "indexation_content": output_metadata,
        })

        return {
            "entities": [
                ENTITY
            ],
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "url", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
