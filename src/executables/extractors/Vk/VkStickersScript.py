from executables.extractors.Base.IterableBase import IterableBase
from executables.extractors.Web.WebURL import WebURL
from resources.Globals import logger

class VkStickersScript(IterableBase):
    name = 'VkStickersScript'
    category = 'Vk'
    docs = {
        "description": {
            "name": {
                "ru": "VK Промежуток стикеров/подарков",
                "en": "VK Range of stickers/gifts"
            },
            "definition": {
                "ru": "Промежуток картинок стикеров или подарков из vk",
                "en": "Metainfo about VK poll"
            }
        }
    }
    file_containment = {
        "files_count": "0-1",
        "files_extensions": ["jpg"]
    }

    def declare():
        params = {}
        params["size"] = {
            "type": "int",
            "default": 512,
            "assertion": {
                "assert_not_null": True,
            }
        }
        params["type"] = {
            "type": "array",
            "values": ["stickers", "gifts"],
            "default": "stickers",
            "assertion": {
                "assert_not_null": True,
            },
        }

        return params

    def _collection(self):
        return {
            "suggested_name": f"Vk Stickers Images {self.passed_params.get("start")}-{self.passed_params.get("end")}",
        }

    async def _iterableAction(self, i):
        if self.passed_params.get("type") == "stickers":
            PATH_URL = (f"https://vk.com/sticker/1-{str(i)}-{str(self.passed_params.get("size"))}.png")
        else:
            PATH_URL = (f"https://vk.com/images/gift/{str(i)}/256.jpg")

        __EXTR = self.fork("Web.WebURL", {
            "url": PATH_URL,
            "make_preview": 0,
        })
        __ent_res = await __EXTR.execute({})
        self.entity_list.append(__ent_res.get("entities")[0])

        logger.log(f"Downloaded URL {PATH_URL}", "IterableBase!VkStickers", "success")
