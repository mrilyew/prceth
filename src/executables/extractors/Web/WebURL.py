from executables.extractors.Base import BaseExtractor
from resources.Globals import os, download_manager, Path, utils, requests, mimetypes, config, file_manager
from resources.Exceptions import NotPassedException
from db.File import File

# Base URL downloader. Downloads single file, without styles, images or something.
class WebURL(BaseExtractor):
    name = 'WebURL'
    category = 'Web'
    manual_params = True
    
    def declare():
        params = {}
        params["url"] = {
            "desc_key": "-",
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }

        return params
    
    async def run(self, args = {}):
        TEMP_DIR = self.allocateTemp()

        PASSED_URL = self.passed_params.get("url")
        name, ext = utils.nameFromURL(PASSED_URL)

        # Making HTTP request
        save_path = Path(os.path.join(TEMP_DIR, "download.tmp"))
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
        
        JOINED_FILE_NAME = '.'.join([name, ext])
        NEW_SAVE_PATH = Path(os.path.join(TEMP_DIR, JOINED_FILE_NAME))
        save_path.rename(os.path.join(TEMP_DIR, NEW_SAVE_PATH))
        file_size = NEW_SAVE_PATH.stat().st_size

        output_metadata = {
            "original_url": str(self.passed_params.get("url")), 
            "mime": str(MIME_EXT),
            "output_name": str(JOINED_FILE_NAME),
        }
        FILE = self._fileFromJson({
            "extension": ext,
            "upload_name": JOINED_FILE_NAME,
            "filesize": file_size,
        })
        ENTITY = self._entityFromJson({
            "file": FILE,
            "source": "url:"+self.passed_params.get("url"),
            "internal_content": output_metadata,
        }, make_preview=self.passed_params.get("make_preview") == 1)

        return {
            "entities": [
                ENTITY
            ],
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "url", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
