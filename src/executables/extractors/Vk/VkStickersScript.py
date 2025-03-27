from executables.extractors.Base import BaseExtractor
from executables.extractors.Web.WebURL import WebURL
from resources.Globals import asyncio, download_manager, logger, storage
from db.File import File

class VkStickersScript(BaseExtractor):
    name = 'VkStickersScript'
    category = 'Vk'
    params = {
        "start": {
            "desc_key": "vk_stickers_start_desc",
            "type": "int",
        },
    }

    def setArgs(self, args):
        self.passed_params["start"] = int(args.get("start", 1))
        self.passed_params["end"] = int(args.get("end", 100))
        self.passed_params["size"] = int(args.get("size", "512"))
        self.passed_params["timeout"] = float(args.get("timeout", "1"))

        super().setArgs(args)

    async def run(self, args):
        entity_list = []

        for i_sticker in range(self.passed_params.get("start"), self.passed_params.get("end")):
            try:
                PATH_URL = (f"https://vk.com/sticker/1-{str(i_sticker)}-{str(self.passed_params.get("size"))}.png")

                __EXTR = WebURL()
                __EXTR.setArgs({
                    "url": PATH_URL,
                    "make_preview": 0,
                })
                __ent_res = await __EXTR.execute({})
                entity_list.append(__ent_res.get("entities")[0])

                logger.log(f"Downloaded URL {PATH_URL}", "VkStickersScript", "success")
            except Exception as ____e:
                logger.logException(____e, "VkStickersScript")

            await asyncio.sleep(self.passed_params.get("timeout"))

        return {
            "entities": entity_list,
            "collection": {
                "suggested_name": f"VK Stickers {self.passed_params.get("start")}-{self.passed_params.get("end")}",
            },
        }
