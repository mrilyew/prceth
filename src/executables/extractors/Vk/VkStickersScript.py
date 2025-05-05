from executables.extractors.Base.IterableBase import IterableBase
from executables.extractors.Web.WebURL import WebURL
from resources.Globals import logger

class VkStickersScript(IterableBase):
    name = 'VkStickersScript'
    category = 'Vk'

    def declare():
        params = {}
        params["size"] = {
            "type": "int",
            "desc_key": "-",
            "default": 512,
            "assertion": {
                "assert_not_null": True,
            }
        }

        return params

    def _collection(self):
        return {
            "suggested_name": f"Vk Stickers Images {self.passed_params.get("start")}-{self.passed_params.get("end")}",
        }

    async def _iterableAction(self, i):
        PATH_URL = (f"https://vk.com/sticker/1-{str(i)}-{str(self.passed_params.get("size"))}.png")

        __EXTR = WebURL()
        __EXTR.setArgs({
            "url": PATH_URL,
            "make_preview": 0,
        })
        __ent_res = await __EXTR.execute({})
        self.entity_list.append(__ent_res.get("entities")[0])

        logger.log(f"Downloaded URL {PATH_URL}", "IterableBase!VkStickers", "success")
