from resources.Globals import Path, download_manager, logger, os
from executables.extractors.Vk.VkBase import VkBase
from resources.Exceptions import NotFoundException

class VkLink(VkBase):
    name = 'VkLink'
    category = 'Vk'
    hidden = True

    def declare():
        params = {}
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "assertion": {
                "assert_not_null": True
            }
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }

        return params
        
    async def run(self, args):
        __json = self.passed_params.get("__json_info")
        if __json == None:
            raise NotFoundException("link not found")
        
        __json["site"] = self.passed_params.get("vk_path")

        logger.log(message=f"Recieved attached link",section="VkAttachments",name="message")
        __FILE = None

        if self.passed_params.get("download_file") == True:
            attached_photo = __json.get("photo")
            if attached_photo != None:
                PHOTO_ID = f"{attached_photo.get("owner_id")}_{attached_photo.get("id")}"
                ORIGINAL_NAME = f"link_photo_{PHOTO_ID}.jpg"
                try:
                    TEMP_DIR = self.allocateTemp()

                    __photo_sizes = sorted(__json.get("photo").get("sizes"), key=lambda x: (x['width'] is None, x['width']), reverse=True)
                    __optimal_size = __photo_sizes[0]

                    SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))
                    HTTP_REQUEST = await download_manager.addDownload(end=__optimal_size.get("url"),dir=SAVE_PATH)
                    FILE_SIZE = SAVE_PATH.stat().st_size
                    __FILE = self._fileFromJson({
                        "extension": "jpg",
                        "upload_name": ORIGINAL_NAME,
                        "filesize": FILE_SIZE,
                    }, TEMP_DIR)

                    __json["relative_photo"] = f"__lcms|file_{__FILE.id}"

                    logger.log(message=f"Downloaded link's photo {PHOTO_ID}",section="VK",name="success")
                except FileNotFoundError as _ea:
                    pass
                    logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VK",name="error")
                
        ENTITY = self._entityFromJson({
            "internal_content": __json,
            "source": f"url:{__json.get('url')}",
            "unlisted": self.passed_params.get('unlisted') == 1,
            "suggested_name": f"Vk Attached link",
            "linked_files": [__FILE]
        })

        return {
            "entities": [ENTITY]
        }
