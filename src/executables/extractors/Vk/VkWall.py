from executables.extractors.Base import BaseExtractor
from executables.extractors.Vk.VkPost import VkPost
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import config, VkApi, logger, utils, math, asyncio

class VkWall(VkTemplate):
    name = 'VkWall'
    category = 'Vk'

    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["filter"] = args.get("filter")
        self.passed_params["download_timeout"] = int(args.get("timeout", "0"))
        self.passed_params["api_timeout"] = int(args.get("timeout", "0"))
        self.passed_params["limit"] = int(args.get("limit", "0"))
        self.passed_params["download_external_media"] = int(args.get("download_external_media", "1"))

        assert self.passed_params.get("item_id") != None, "item_id not passed"

        super().setArgs(args)

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        __temp_final_params = {"owner_id": self.passed_params.get("item_id"), "count": 1}
        if self.passed_params.get("filter") != None:
            __temp_final_params["filter"] = self.passed_params.get("filter")
        
        first_call = await __vkapi.call("wall.get", __temp_final_params)
        total_count = first_call.get("count")
        final_entites_list = []

        logger.log(message=f"Total {total_count} posts",section="VkCollection",name="message")

        __per_page = 100
        __downloaded_count = 0
        times = math.ceil(total_count / __per_page)
        for time in range(0, times):
            OFFSET = __per_page * time
            if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                break
            
            logger.log(message=f"{time + 1}/{times} time of posts recieving; {OFFSET} offset",section="VkCollection",name="message")
            
            __post_call_params = {"owner_id": self.passed_params.get("item_id"), "extended": 1, "count": 100, "photo_sizes": 1, "offset": OFFSET}
            if self.passed_params.get("filter") != None:
                __post_call_params["filter"] = self.passed_params.get("filter")
            
            post_call = await __vkapi.call("wall.get", __post_call_params)
            for post_item in post_call.get("items"):
                if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                    break
                
                __POST_ID = str(post_item.get("owner_id")) + "_" + str(post_item.get("id"))
                vpost_ext = VkPost(need_preview=self.need_preview)
                vpost_ext.setArgs({
                    "unlisted": 1,
                    "item_id": __POST_ID,
                    "__json_info": post_item,
                    "__json_profiles": __post_call_params.get("profiles"),
                    "__json_groups": __post_call_params.get("groups"),
                    "access_token": self.passed_params.get("access_token"),
                    "api_url": self.passed_params.get("api_url"),
                    "vk_path": self.passed_params.get("vk_path"),
                    "download_external_media": self.passed_params.get("download_external_media"),
                })

                try:
                    executed = await vpost_ext.execute({})
                    for __post in executed.get("entities"):
                        final_entites_list.append(__post)
                except Exception as _ae:
                    logger.logException(_ae, section="VkCollection")
                
                del vpost_ext

                if self.passed_params.get("download_timeout") != 0:
                    await asyncio.sleep(self.passed_params.get("download_timeout"))

                __downloaded_count += 1
            
            if self.passed_params.get("api_timeout") != 0:
                await asyncio.sleep(self.passed_params.get("api_timeout"))
        
        return {
            "entities": final_entites_list,
            "collection": {
                "suggested_name": f"Vk Wall {self.passed_params.get("item_id")}",
            },
        }
