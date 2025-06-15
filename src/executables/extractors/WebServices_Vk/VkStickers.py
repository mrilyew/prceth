from executables.extractors.Base.IterableBase import IterableBase
from declarable.ArgumentsTypes import IntArgument, LimitedArgument
from representations.Data.File import File
from app.App import logger

class VkStickers(IterableBase):
    category = 'WebServices_Vk'

    def declare():
        params = {}
        params["size"] = IntArgument({
            "default": 512,
            "assertion": {
                "not_null": True,
            }
        })
        params["type"] = LimitedArgument({
            "values": ["stickers", "gifts"],
            "default": "stickers",
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def _iterableAction(self, i, iterator):
        if i.get("type") == "stickers":
            PATH_URL = (f"https://vk.com/sticker/1-{str(iterator)}-{str(i.get("size"))}.png")
        else:
            PATH_URL = (f"https://vk.com/images/gift/{str(iterator)}/256.jpg")

        __extrs = await File.extract({
            "url": PATH_URL,
        })

        for item in __extrs:
            self.linked_dict.append(item)

        logger.log(f"Downloaded URL {PATH_URL}", "Iterable!VkStickers", "success")
