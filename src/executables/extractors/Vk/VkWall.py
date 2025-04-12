from executables.extractors.Base import BaseExtractor
from executables.extractors.Vk.VkPost import VkPost
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import config, VkApi, logger, utils, math, asyncio

class VkWall(VkTemplate):
    name = 'VkWall'
    category = 'Vk'
    
    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["filter"] = {
            "desc_key": "-",
            "type": "array",
            "values": ["suggests", "postponed", "owner", "others", "all", "donut", "archived"],
            "default": "all",
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["download_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["api_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["download_attachments_json_list"] = {
            "desc_key": "-",
            "type": "string",
            "default": "*",
        }
        params["download_attachments_file_list"] = {
            "desc_key": "-",
            "type": "string",
            "default": "photo",
        }
        params["download_reposts"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }
        params["limit"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0
        }
        params["per_page"] = {
            "desc_key": "-",
            "type": "int",
            "default": 100
        }

        return params

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        __temp_final_params = {"owner_id": self.passed_params.get("item_id"), "count": 1}
        if self.passed_params.get("filter") != None:
            __temp_final_params["filter"] = self.passed_params.get("filter")
        
        first_call = await __vkapi.call("wall.get", __temp_final_params)
        total_count = first_call.get("count")
        final_entites_list = []

        logger.log(message=f"Total {total_count} posts",section="VkCollection",name="message")

        __per_page = self.passed_params.get("per_page")
        __downloaded_count = 0
        times = math.ceil(total_count / __per_page)
        vpost_ext = VkPost(need_preview=self.need_preview)

        for time in range(0, times):
            OFFSET = __per_page * time
            if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                break
            
            logger.log(message=f"{time + 1}/{times} time of posts recieving; {OFFSET} offset",section="VkCollection",name="message")
            
            __post_call_params = {"owner_id": self.passed_params.get("item_id"), "extended": 1, "count": __per_page, "photo_sizes": 1, "offset": OFFSET}
            if self.passed_params.get("filter") != None:
                __post_call_params["filter"] = self.passed_params.get("filter")
            
            post_call = await __vkapi.call("wall.get", __post_call_params)
            for post_item in post_call.get("items"):
                if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                    break
                
                __POST_ID = str(post_item.get("owner_id")) + "_" + str(post_item.get("id"))
                vpost_ext.setArgs({
                    "unlisted": 1,
                    "item_id": __POST_ID,
                    "__json_info": post_item,
                    "__json_profiles": __post_call_params.get("profiles"),
                    "__json_groups": __post_call_params.get("groups"),
                    "download_attachments_json_list": self.passed_params.get("download_attachments_json_list"),
                    "download_attachments_file_list": self.passed_params.get("download_attachments_file_list"),
                    "download_reposts": self.passed_params.get("download_reposts"),
                    "download_comments": False,
                    "access_token": self.passed_params.get("access_token"),
                    "api_url": self.passed_params.get("api_url"),
                    "vk_path": self.passed_params.get("vk_path"),
                })

                try:
                    executed = await vpost_ext.execute({})
                    for __post in executed.get("entities"):
                        final_entites_list.append(__post)
                except Exception as _ae:
                    logger.logException(_ae, section="VkCollection")

                if self.passed_params.get("download_timeout") != 0:
                    await asyncio.sleep(self.passed_params.get("download_timeout"))

                __downloaded_count += 1
            
            if self.passed_params.get("api_timeout") != 0:
                await asyncio.sleep(self.passed_params.get("api_timeout"))
        
        await vpost_ext.postRun(final_entites_list)
        del vpost_ext

        return {
            "entities": final_entites_list,
            "collection": {
                "suggested_name": f"Vk Wall {self.passed_params.get("item_id")}",
            },
        }
