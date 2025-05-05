from executables.extractors.Vk.VkBase import VkBase
from executables.extractors.Files.JsonObject import JsonObject
from resources.Globals import VkApi, json, utils, ExtractorsRepository, logger, asyncio
from resources.Exceptions import NotFoundException

class VkPost(VkBase):
    name = 'VkPost'
    category = 'Vk'
    vk_type = "post"

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

    async def recieveById(self, post_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("wall.getById", {"posts": ",".join(post_ids), "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/wall1_1
        __POST_RESPONSE = None
        ITEM_IDS_STR = self.passed_params.get("item_id", "")
        ITEM_IDS = ITEM_IDS_STR.split(",")

        if self.passed_params.get("__json_info") == None:
            assert len(ITEM_IDS) > 0, "item_id's not passed("
            __POST_RESPONSE = await self.recieveById(ITEM_IDS)
            self.__profiles = __POST_RESPONSE.get("profiles")
            self.__groups = __POST_RESPONSE.get("groups")
        else:
            __POST_RESPONSE = self.passed_params.get("__json_info", None)
            self.__profiles = __POST_RESPONSE.get("__json_profiles")
            self.__groups = __POST_RESPONSE.get("__json_groups")

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
        
        __entities_list = []
        __tasks = []
        for post in __POST_ITEMS:
            __task = asyncio.create_task(self.__item(post, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)
        
        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        DOWNLOAD_JSON_LIST = self.passed_params.get("download_attachments_json_list").split(",")
        DOWNLOAD_FILE_LIST = self.passed_params.get("download_attachments_file_list").split(",")

        item["site"] = self.passed_params.get("vk_path")
        item["relative_attachments"] = {}
        item["relative_copy_history"] = {}

        ITEM_ID = f"{item.get('owner_id')}_{item.get('id')}"
        __SOURCE = "vk:wall"+ITEM_ID
        if self.vk_type == "message":
            ITEM_ID = f"{item.get('peer_id', item.get("from_id"))}_{item.get('id')}"
            __SOURCE = "vk:message"+ITEM_ID

        item.pop("track_code", None)
        item.pop("hash", None)

        logger.log(message=f"Recieved {self.vk_type} {ITEM_ID}",section="VK",name="message")

        __linked_files = []
        for key, attachment in enumerate(item.get("attachments", [])):
            try:
                __attachment_type = attachment.get("type")
                __attachment_class_name = __attachment_type
                __attachment_object = attachment.get(__attachment_type)
                if __attachment_object == None:
                    continue
                
                if __attachment_type == "wall":
                    __attachment_class_name = "post"
                
                should_download_json = DOWNLOAD_JSON_LIST[0] == "*" or __attachment_type in DOWNLOAD_JSON_LIST
                should_download_file = DOWNLOAD_FILE_LIST[0] == "*" or __attachment_type in DOWNLOAD_FILE_LIST
                
                if should_download_json == False:
                    continue
                
                __attachment_class = (ExtractorsRepository().getByName(f"Vk.Vk{__attachment_class_name.title()}"))
                if __attachment_class == None:
                    logger.log(message="Recieved unknown attachment: " + str(__attachment_class_name),section="VkAttachments",name="message")

                    __attachment_class_unknown = JsonObject()
                    __attachment_class_unknown.setArgs({
                        "json_object": item["attachments"][key][__attachment_class_name],
                    })

                    __attachment_class_unknown_entities = await __attachment_class_unknown.execute({})
                    __attachment_class_entity = __attachment_class_unknown_entities.get("entities")[0]

                    __linked_files.append(__attachment_class_entity)
                    item["relative_attachments"][key][__attachment_class_name] = f"__lcms|entity_{__attachment_class_entity.id}"
                else:
                    ATTACHMENT_ID = f"{__attachment_object.get('owner_id')}_{__attachment_object.get('id')}"
                    logger.log(message=f"Recieved attachment {str(__attachment_class_name)} {ATTACHMENT_ID}",section="VkAttachments",name="message")

                    __attachment_class_dec = __attachment_class(need_preview=self.need_preview)
                    __attachment_class_return = await __attachment_class_dec.fastGetEntity(params={
                        "unlisted": 1,
                        "item_id": ATTACHMENT_ID,
                        "__json_info": __attachment_object,
                        "access_token": self.passed_params.get("access_token"),
                        "api_url": self.passed_params.get("api_url"),
                        "vk_path": self.passed_params.get("vk_path"),
                        "download_file": should_download_file,
                    },args={})

                    __linked_files.append(__attachment_class_return[0])
                    item["relative_attachments"][key][__attachment_class_name] = f"__lcms|entity_{__attachment_class_return[0].id}"
            except ModuleNotFoundError:
                pass
            except Exception as ___e___:
                logger.logException(___e___, "VkAttachments")

        if item.get("copy_history") != None and self.passed_params.get("download_reposts") == True:
            for key, repost in enumerate(item.get("copy_history")):
                try:
                    REPOST_ID = f"{repost.get('owner_id')}_{repost.get('id')}"
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
                    },args={})

                    __linked_files.append(__vk_post_entity[0])
                    item["relative_copy_history"][key] = f"__lcms|entity_{__vk_post_entity[0].id}"
                except ModuleNotFoundError:
                    pass
                except Exception as ___e___:
                    logger.logException(___e___, "VkAttachments")

        if item.get("from_id") != None and self.__profiles != None:
            item["from"] = utils.find_owner(item.get("from_id"), self.__profiles, self.__groups)
        if item.get("owner_id") != None and self.__profiles != None:
            item["owner"] = utils.find_owner(item.get("owner_id"), self.__profiles, self.__groups)
        if item.get("copy_owner_id") != None and self.__profiles != None:
            item["copy_owner"] = utils.find_owner(item.get("copy_owner_id"), self.__profiles, self.__groups)

        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "suggested_name": f"VK {self.vk_type.title()} {str(ITEM_ID)}",
            "internal_content": item,
            "linked_files": __linked_files,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
        })
        link_entities.append(ENTITY)
