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

        return params

    async def __recieveById(self, post_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("wall.getById", {"posts": ",".join(post_ids), "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/wall1_1
        __POST_RESPONSE = None
        __PROFILES = None
        __GROUPS   = None
        ITEM_IDS_STR = self.passed_params.get("item_id", "")
        ITEM_IDS = ITEM_IDS_STR.split(",")

        if self.passed_params.get("__json_info") == None:
            assert len(ITEM_IDS) > 0, "item_id's not passed("
            __POST_RESPONSE = await self.__recieveById(ITEM_IDS)
            __PROFILES = __POST_RESPONSE.get("profiles")
            __GROUPS = __POST_RESPONSE.get("groups")
        else:
            __POST_RESPONSE = self.passed_params.get("__json_info", None)
            __PROFILES = __POST_RESPONSE.get("__json_profiles")
            __GROUPS = __POST_RESPONSE.get("__json_groups")
        
        __POST_ITEMS = []
        try:
            if __POST_RESPONSE.get("items") != None:
                __POST_ITEMS = __POST_RESPONSE.get("items")
            else:
                __POST_ITEMS = [__POST_RESPONSE]
        except Exception:
            __POST_ITEMS = None

        if __POST_ITEMS == None:
            raise NotFoundException("post items not found")
        
        DOWNLOAD_JSON_LIST = self.passed_params.get("download_attachments_json_list").split(",")
        DOWNLOAD_FILE_LIST = self.passed_params.get("download_attachments_file_list").split(",")

        final_entities = []
        for post in __POST_ITEMS:
            post["site"] = self.passed_params.get("vk_path")
            post["relative_attachments"] = {}
            post["relative_copy_history"] = {}

            ITEM_ID = f"{post.get("owner_id")}_{post.get("id")}"

            post.pop("track_code", None)
            post.pop("hash", None)

            logger.log(message=f"Recieved post {ITEM_ID}",section="VK",name="message")
            
            __linked_files = []
            for key, attachment in enumerate(post.get("attachments")):
                try:
                    __attachment_type = attachment.get("type")
                    __attachment_object = attachment.get(__attachment_type)
                    if __attachment_object == None:
                        continue
                    
                    should_download_json = DOWNLOAD_JSON_LIST[0] == "*" or __attachment_type in DOWNLOAD_JSON_LIST
                    should_download_file = DOWNLOAD_FILE_LIST[0] == "*" or __attachment_type in DOWNLOAD_FILE_LIST
                    
                    if should_download_json == False:
                        continue
                    
                    __attachment_class = (ExtractorsRepository().getByName(f"Vk.Vk{__attachment_type.title()}"))
                    if __attachment_class == None:
                        logger.log(message="Recieved unknown attachment: " + str(__attachment_type),section="VkAttachments",name="message")

                        __attachment_class_unknown = JsonObject()
                        __attachment_class_unknown.setArgs({
                            "json_object": post["attachments"][key][__attachment_type],
                        })

                        __attachment_class_unknown_entities = await __attachment_class_unknown.execute({})
                        __attachment_class_entity = __attachment_class_unknown_entities.get("entities")[0]

                        __linked_files.append(__attachment_class_entity)
                        post["relative_attachments"][key][__attachment_type] = f"__lcms|entity_{__attachment_class_entity.id}"
                    else:
                        ATTACHMENT_ID = f"{__attachment_object.get("owner_id")}_{__attachment_object.get("id")}"
                        logger.log(message=f"Recieved attachment {str(__attachment_type)} {ATTACHMENT_ID}",section="VkAttachments",name="message")
                        
                        __attachment_class_dec = __attachment_class(need_preview=self.need_preview)
                        __attachment_class_return = await __attachment_class_dec.fastGetEntity(params={
                            "unlisted": 1,
                            "item_id": ATTACHMENT_ID,
                            "__json_info": __attachment_object,
                            "access_token": self.passed_params.get("access_token"),
                            "api_url": self.passed_params.get("api_url"),
                            "vk_path": self.passed_params.get("vk_path"),
                            "download_file": should_download_file,
                        },args=args)

                        __linked_files.append(__attachment_class_return[0])
                        post["relative_attachments"][key][__attachment_type] = f"__lcms|entity_{__attachment_class_return[0].id}"
                except ModuleNotFoundError:
                    pass
                except Exception as ___e___:
                    logger.logException(___e___, "VkAttachments")

            if post.get("copy_history") != None and self.passed_params.get("download_reposts") == True:
                for key, repost in enumerate(post.get("copy_history")):
                    try:
                        REPOST_ID = f"{repost.get("owner_id")}_{repost.get("id")}"
                        if repost == None:
                            continue
                        
                        logger.log(message=f"Found repost {key}",section="VKPost",name="message")

                        __vk_post_extractor = VkPost(need_preview=self.need_preview)
                        __vk_post_entity = await __vk_post_extractor.fastGetEntity(params={
                            "unlisted": 1,
                            "item_id": REPOST_ID,
                            "__json_info": repost,
                            "access_token": self.passed_params.get("access_token"),
                            "api_url": self.passed_params.get("api_url"),
                            "vk_path": self.passed_params.get("vk_path"),
                            "download_attachments_json_list": self.passed_params.get("download_attachments_json_list"),
                            "download_attachments_file_list": self.passed_params.get("download_attachments_file_list"),
                            "download_reposts": False,
                        },args=args)

                        __linked_files.append(__vk_post_entity[0])
                        post["relative_copy_history"][key] = f"__lcms|entity_{__vk_post_entity[0].id}"
                    except ModuleNotFoundError:
                        pass
                    except Exception as ___e___:
                        logger.logException(___e___, "VkAttachments")
            
            if post.get("from_id") != None and __PROFILES != None:
                post["from"] = utils.find_owner(post.get("from_id"), __PROFILES, __GROUPS)
            if post.get("owner_id") != None and __PROFILES != None:
                post["owner"] = utils.find_owner(post.get("owner_id"), __PROFILES, __GROUPS)
            if post.get("copy_owner_id") != None and __PROFILES != None:
                post["copy_owner"] = utils.find_owner(post.get("copy_owner_id"), __PROFILES, __GROUPS)

            ENTITY = self._entityFromJson({
                "source": "vk:wall"+ITEM_ID,
                "suggested_name": f"VK Post {str(ITEM_ID)}",
                "internal_content": post,
                "linked_files": __linked_files,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": post.get("date"),
            })
            final_entities.append(ENTITY)
        
        return {
            "entities": final_entities
        }
