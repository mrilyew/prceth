from executables.extractors.Base import BaseExtractor
from resources.Globals import VkApi, json, utils, config, ExtractorsRepository, storage, logger
from resources.Exceptions import NotFoundException

class VkPost(BaseExtractor):
    name = 'VkPost'
    category = 'Vk'

    def passParams(self, args):
        self.passed_params = args
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["access_token"] = args.get("access_token", config.get("vk.access_token", None))
        self.passed_params["api_url"] = args.get("api_url", "api.vk.com/method")
        self.passed_params["vk_path"] = args.get("vk_path", "vk.com")

        assert self.passed_params.get("item_id") != None, "item_id not passed"
        assert self.passed_params.get("access_token") != None, "access_token not passed"
        assert self.passed_params.get("api_url") != None, "api_url not passed"
        assert self.passed_params.get("vk_path") != None, "vk_path not passed"

        super().passParams(args)

    async def __recieveById(self, photo_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("wall.getById", {"posts": photo_id, "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/wall1_1
        __post_api_response = None
        __item_id  = self.passed_params.get("item_id")
        if getattr(self, "__predumped_info", None) == None:
            __post_api_response = await self.__recieveById(__item_id)
        else:
            __post_api_response = self.__predumped_info
        
        # TODO: Attachments processing
        try:
            __POST_OBJ = __post_api_response.get("items")[0]
            __item_id = f"{__POST_OBJ.get("owner_id")}_{__POST_OBJ.get("id")}"
            __POST_OBJ.pop("track_code", None)
            __POST_OBJ.pop("hash", None)
        
        except Exception:
            __POST_OBJ = None

        if __POST_OBJ == None:
            raise NotFoundException("post not found")

        logger.log(message=f"Recieved post {__item_id}",section="VK",name="message")

        # Making indexation
        __POST_OBJ["site"] = self.passed_params.get("vk_path")
        __indexation = utils.clearJson(__POST_OBJ)

        linked_files = []
        for key, attachment in enumerate(__POST_OBJ.get("attachments")):
            try:
                __attachment_type = attachment.get("type")
                __attachment_object = attachment.get(__attachment_type)
                if __attachment_object == None:
                    continue

                EXTRACTOR_INSTANCE_CLASS = (ExtractorsRepository().getByName(f"Vk.Vk{__attachment_type.title()}"))
                if EXTRACTOR_INSTANCE_CLASS == None:
                    logger.log(message="Unknown attachment: " + str(__attachment_object),section="VkAttachments",name="message")
                    continue

                EXPORT_DIRECTORY = storage.makeTemporaryCollectionDir()
                EXTRACTOR_INSTANCE = EXTRACTOR_INSTANCE_CLASS(temp_dir=EXPORT_DIRECTORY)
                RETURN_ENTITY = await EXTRACTOR_INSTANCE.fastGetEntity(params={
                    "is_hidden": True,
                    "item_id": f"{__attachment_object.get("owner_id")}_{__attachment_object.get("id")}",
                    "preset_json": __attachment_object,
                    "access_token": self.passed_params.get("access_token"),
                    "api_url": self.passed_params.get("api_url"),
                    "vk_path": self.passed_params.get("vk_path"),
                },args=args)

                linked_files.append(RETURN_ENTITY.id)
                __POST_OBJ["attachments"][key][__attachment_type] = f"__lcms|entity_{RETURN_ENTITY.id}"
            except ModuleNotFoundError:
                pass
            except Exception as ___e___:
                logger.logException(___e___, "VkAttachment")
        
        return {
            "entities": [
                {
                    "source": "vk:wall"+__item_id,
                    "suggested_name": f"VK Post {str(__item_id)}",
                    "indexation_content": __indexation,
                    "entity_internal_content": __POST_OBJ,
                    "linked_files": linked_files,
                }
            ]
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get("vk_path")}/" + INPUT_ENTITY.orig_source
        }}
