from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Files.JsonObject import JsonObject
from resources.Globals import VkApi, json, utils, config, ExtractorsRepository, storage, logger
from resources.Exceptions import NotFoundException

class VkPost(VkTemplate):
    name = 'VkPost'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }
        params["__json_profiles"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
        }
        params["__json_groups"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
        }
        params["download_external_media"] = {
            "desc_key": "-",
            "type": "bool",
            "default": "0"
        }

        return params

    async def __recieveById(self, post_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("wall.getById", {"posts": post_id, "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/wall1_1
        __POST_RESPONSE = None
        __PROFILES = None
        __GROUPS   = None
        ITEM_ID = self.passed_params.get("item_id")
        if self.passed_params.get("__json_info", None) == None:
            __POST_RESPONSE = await self.__recieveById(ITEM_ID)
            __PROFILES = __POST_RESPONSE.get("profiles")
            __GROUPS = __POST_RESPONSE.get("groups")
        else:
            __POST_RESPONSE = self.passed_params.get("__json_info", None)
            __PROFILES = __POST_RESPONSE.get("__json_profiles")
            __GROUPS = __POST_RESPONSE.get("__json_groups")
        
        try:
            __POST_OBJ = None

            if __POST_RESPONSE.get("items") != None:
                __POST_OBJ = __POST_RESPONSE.get("items")[0]
            else:
                __POST_OBJ = __POST_RESPONSE
            
            __POST_OBJ.pop("track_code", None)
            __POST_OBJ.pop("hash", None)

            ITEM_ID = f"{__POST_OBJ.get("owner_id")}_{__POST_OBJ.get("id")}"
        except Exception:
            __POST_OBJ = None

        if __POST_OBJ == None:
            raise NotFoundException("post not found")

        logger.log(message=f"Recieved post {ITEM_ID}",section="VK",name="message")

        # Making indexation
        __POST_OBJ["site"] = self.passed_params.get("vk_path")

        linked_files = []
        for key, attachment in enumerate(__POST_OBJ.get("attachments")):
            try:
                __attachment_type = attachment.get("type")
                __attachment_object = attachment.get(__attachment_type)
                if __attachment_object == None:
                    continue

                EXTRACTOR_INSTANCE_CLASS = (ExtractorsRepository().getByName(f"Vk.Vk{__attachment_type.title()}"))
                if EXTRACTOR_INSTANCE_CLASS == None:
                    RET_EXT = JsonObject()
                    RET_EXT.setArgs({
                        "json_object": __POST_OBJ["attachments"][key][__attachment_type],
                    })

                    ENTITIES = await RET_EXT.execute({})
                    __ENTITY = ENTITIES.get("entities")[0]

                    linked_files.append(__ENTITY)
                    __POST_OBJ["attachments"][key][__attachment_type] = f"__lcms|entity_{__ENTITY.id}"

                    logger.log(message="Unknown attachment: " + str(__attachment_object),section="VkAttachments",name="message")
                    continue

                EXTRACTOR_INSTANCE = EXTRACTOR_INSTANCE_CLASS(need_preview=self.need_preview)
                RETURN_ENTITY = await EXTRACTOR_INSTANCE.fastGetEntity(params={
                    "unlisted": 1,
                    "item_id": f"{__attachment_object.get("owner_id")}_{__attachment_object.get("id")}",
                    "__json_info": __attachment_object,
                    "access_token": self.passed_params.get("access_token"),
                    "api_url": self.passed_params.get("api_url"),
                    "vk_path": self.passed_params.get("vk_path"),
                    "download_file": self.passed_params.get("download_external_media"),
                },args=args)

                linked_files.append(RETURN_ENTITY[0])
                __POST_OBJ["attachments"][key][__attachment_type] = f"__lcms|entity_{RETURN_ENTITY[0].id}"
            except ModuleNotFoundError:
                pass
            except Exception as ___e___:
                logger.logException(___e___, "VkAttachments")

        if __POST_OBJ.get("copy_history") != None:
            for key, repost in enumerate(__POST_OBJ.get("copy_history")):
                try:
                    if repost == None:
                        continue
                    
                    logger.log(message=f"Found repost {key}",section="VKPost",name="message")
                    EXTRACTOR_INSTANCE = VkPost(need_preview=self.need_preview)
                    RETURN_ENTITY = await EXTRACTOR_INSTANCE.fastGetEntity(params={
                        "unlisted": 1,
                        "item_id": f"{repost.get("owner_id")}_{repost.get("id")}",
                        "__json_info": repost,
                        "access_token": self.passed_params.get("access_token"),
                        "api_url": self.passed_params.get("api_url"),
                        "vk_path": self.passed_params.get("vk_path"),
                        "download_external_media": self.passed_params.get("download_external_media"),
                    },args=args)

                    linked_files.append(RETURN_ENTITY[0])
                    __POST_OBJ["copy_history"][key] = f"__lcms|entity_{RETURN_ENTITY[0].id}"
                except ModuleNotFoundError:
                    pass
                except Exception as ___e___:
                    logger.logException(___e___, "VkAttachments")
        
        if __POST_OBJ.get("from_id") != None and __PROFILES != None:
            __POST_OBJ["from"] = utils.find_owner(__POST_OBJ.get("from_id"), __PROFILES, __GROUPS)
        if __POST_OBJ.get("owner_id") != None and __PROFILES != None:
            __POST_OBJ["owner"] = utils.find_owner(__POST_OBJ.get("owner_id"), __PROFILES, __GROUPS)
        if __POST_OBJ.get("copy_owner_id") != None and __PROFILES != None:
            __POST_OBJ["copy_owner"] = utils.find_owner(__POST_OBJ.get("copy_owner_id"), __PROFILES, __GROUPS)
        
        ENTITY = self._entityFromJson({
            "source": "vk:wall"+ITEM_ID,
            "suggested_name": f"VK Post {str(ITEM_ID)}",
            "internal_content": __POST_OBJ,
            "linked_files": linked_files,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })
        
        return {
            "entities": [
                ENTITY
            ]
        }
