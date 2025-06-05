from resources.Globals import Path, download_manager, logger, os, media_utils
from executables.extractors.Vk.VkBase import VkBase
from resources.Exceptions import NotFoundException

class VkGraffiti(VkBase):
    name = 'VkGraffiti'
    category = 'Vk'
    hidden = True
    docs = {
        "description": {
            "name": {
                "ru": "VK Граффити",
                "en": "VK Graffiti"
            },
            "definition": {
                "ru": "Граффити из vk",
                "en": "Graffiti from vk"
            }
        },
    }
    file_containment = {
        "files_count": "1",
        "files_extensions": ["png"]
    }

    def declare():
        params = {}
        params["__json_info"] = {
            "type": "object",
            "assertion": {
                "not_null": True
            }
        }
        params["download_file"] = {
            "type": "bool",
            "default": True
        }

        return params

    async def run(self, args):
        __json = self.passed_params.get("__json_info")
        if __json == None:
            raise NotFoundException("graffiti not found")

        __json["site"] = self.passed_params.get("vk_path")

        __ITEM_ID  = f"{__json.get('owner_id')}_{__json.get('id')}"
        __SOURCE   = f"vk:graffiti{__ITEM_ID}"

        logger.log(message=f"Recieved graffiti {__ITEM_ID}",section="VkAttachments",name="message")

        max_size = media_utils.find_highest_in_dict(__json, "photo_")

        if self.passed_params.get("download_file") == True:
            __FILE = None
            try:
                PHOTO_URL = __json.get(f"photo_{max_size}")
                ORIGINAL_NAME = f"graffiti{__ITEM_ID}.png"
                TEMP_DIR = self.allocateTemp()

                SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))
                HTTP_REQUEST = await download_manager.addDownload(end=PHOTO_URL,dir=SAVE_PATH)
                FILE_SIZE = SAVE_PATH.stat().st_size
                __FILE = self._fileFromJson({
                    "extension": "png",
                    "upload_name": ORIGINAL_NAME,
                    "filesize": FILE_SIZE,
                }, TEMP_DIR)

                logger.log(message=f"Downloaded graffiti {__ITEM_ID}",section="VK",name="success")
            except FileNotFoundError as _ea:
                logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VK",name="error")

        ContentUnit = self._ContentUnitFromJson({
            "source": __SOURCE,
            "internal_content": __json,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "suggested_name": f"Graffiti {__json.get('id')}",
            "file": __FILE,
        })

        return {
            "entities": [ContentUnit]
        }
