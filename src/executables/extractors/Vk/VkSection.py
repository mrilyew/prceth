from resources.Globals import config, VkApi, logger, utils, math, asyncio
from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from executables.extractors.Vk.VkPost import VkPost
from resources.Exceptions import InvalidPassedParam

class VkSection(VkTemplate):
    name = 'VkSection'
    category = 'Vk'
    manual_params = True

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["section"] = {
            "desc_key": "-",
            "type": "array",
            "values": ["photos", "wall", "album", "board"],
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
        params["limit"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["per_page"] = {
            "desc_key": "-",
            "type": "int",
            "default": 100
        }
        params["start_range"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0
        }
        params["filter"] = {
            "desc_key": "-",
            "type": "string",
            "default": None,
            "assertion": {
                "only_when": {
                    "section": "wall"
                }
            }
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
        params["download_comments"] = {
            "desc_key": "-",
            "type": "bool",
            "default": False,
        }
        params["rev"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }

        return params
    
    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        __total_count = 0
        __downloaded_count = 0
        __times = 0
        __per_page = self.passed_params.get("per_page")
        __start_range = self.passed_params.get("start_range")
        __method = ""
        __dict_name = "items"
        __final_entities = []
        __has_profile = False
        __pass_params = {}
        __extractor = None
        __extractor_params = {
            "unlisted": 1,
            "access_token": self.passed_params.get("access_token"),
            "api_url": self.passed_params.get("api_url"),
            "vk_path": self.passed_params.get("vk_path"),
            "download_file": 1,
        }

        __item_ids = self.passed_params.get("item_id")
        item_id_collection = __item_ids.split(",")[0]

        __collection = {
            "suggested_name": f"Vk Collection {item_id_collection}",
        }

        # Making first call
        match(self.passed_params.get("section")):
            case "photos":
                __method = "photos.getAll"
                __count_call = await __vkapi.call(__method, {"owner_id": item_id_collection, "count": 1})
                __total_count = __count_call.get("count")
                __extractor = VkPhoto()
                __pass_params = {
                    "owner_id": item_id_collection, 
                    "extended": 1,
                    "photo_sizes": 1
                }
                __collection["suggested_name"] = f"Vk Photos {item_id_collection}"
            case "wall":
                __method = "wall.get"
                __temp_final_params = {"owner_id": item_id_collection, "count": 1}
                if self.passed_params.get("filter") != None:
                    __temp_final_params["filter"] = self.passed_params.get("filter")

                __has_profile = True
                __count_call = await __vkapi.call(__method, __temp_final_params)
                __total_count = __count_call.get("count")
                __extractor = VkPost()
                __extractor_params["download_attachments_json_list"] = self.passed_params.get("download_attachments_json_list")
                __extractor_params["download_attachments_file_list"] = self.passed_params.get("download_attachments_file_list")
                __extractor_params["download_reposts"] = self.passed_params.get("download_reposts")
                __extractor_params["download_comments"] = False
                __pass_params = {
                    "owner_id": item_id_collection, 
                    "extended": 1, 
                    "photo_sizes": 1,
                }
                if self.passed_params.get("filter") != None:
                    __pass_params["filter"] = self.passed_params.get("filter")
                
                __collection["suggested_name"] = f"Vk Wall {item_id_collection}"
            case "album":
                __method = "photos.get"
                __spl = item_id_collection.split("_")
                __owner_id = __spl[0]
                __item_id =  __spl[1]

                match __item_id:
                    case "0":
                        __item_id = "wall"
                    case "00":
                        __item_id = "profile"
                    case "000":
                        __item_id = "saved"
                
                __pass_params = {
                    "owner_id": __owner_id,
                    "album_id": __item_id,
                    "rev": int(self.passed_params.get("rev")), 
                    "extended": 1,
                    "photo_sizes": 1,
                }
                __count_call = await __vkapi.call(__method, {"owner_id": __owner_id, "album_id": __item_id, "count": 1})
                __total_count = __count_call.get("count")
                __extractor = VkPhoto()
                
                __collection["suggested_name"] = f"Vk Album {item_id_collection}"
            case _:
                raise InvalidPassedParam("invalid section")
        
        __times = math.ceil(__total_count / __per_page)

        logger.log(message=f"Total {__total_count} items; will be {__times} calls",section="VkSection",name="message")
        for time in range(__start_range, __times):
            offset = __per_page * time
            if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                break

            logger.log(message=f"{time + 1}/{__times} time of photos recieving; {offset} offset",section="VkCollection",name="message")
           
            __pass_params["count"] = __per_page
            __pass_params["offset"] = offset
            __time_call = await __vkapi.call(__method, __pass_params)

            for item in __time_call.get(__dict_name):
                if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                    break
                
                item_id = str(item.get("owner_id")) + "_" + str(item.get("id"))

                __extractor_params["item_id"] = item_id
                __extractor_params["__json_info"] = item
                
                if __has_profile == True:
                    __extractor_params["__json_profiles"] = __time_call.get("profiles")
                    __extractor_params["__json_groups"] = __time_call.get("groups")
                
                __extractor.setArgs(__extractor_params)

                try:
                    executed = await __extractor.execute({})
                    for ___item in executed.get("entities"):
                        __final_entities.append(___item)
                except Exception as ___e:
                    logger.logException(input_exception=___e,section="VkCollection",noConsole=False)
                    pass

                if self.passed_params.get("download_timeout") != 0:
                    await asyncio.sleep(self.passed_params.get("download_timeout"))

                __downloaded_count += 1
            
            if self.passed_params.get("api_timeout") != 0:
                await asyncio.sleep(self.passed_params.get("api_timeout"))
            
        #await __extractor.postRun(return_entities=__final_entities)
        del __extractor

        return {
            "entities": __final_entities,
            "collection": __collection
        }
