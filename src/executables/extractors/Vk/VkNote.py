from resources.Globals import VkApi, utils, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkNote(VkTemplate):
    name = 'VkNote'
    category = 'Vk'
    params = {
        "item_id": {
            "desc_key": "vk_note_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)
        self.passed_params["indexation_text_cut"] = int(args.get("indexation_text_cut", "699"))

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"

        super().setArgs(args)
    
    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("notes.get", {"note_ids": item_id, "user_id": 1})
    
    async def run(self, args):
        __ITEM_RES = None
        __SOURCE   = None
        NOTE = None
        __ITEM_ID  = self.passed_params.get("item_id")
        if self.passed_params.get("__json_info") == None:
            try:
                __ITEM_RES = await self.__recieveById(__ITEM_ID)
                if __ITEM_RES.get("items") != None:
                    NOTE = __ITEM_RES.get("items")[0]
                else:
                    NOTE = __ITEM_RES.get("notes")[0]
            except:
                NOTE = None
        else:
            try:
                __ITEM_RES = self.passed_params.get("__json_info")
                NOTE = __ITEM_RES
            except:
                NOTE = None

        if NOTE == None:
            raise NotFoundException("note not found")
        
        logger.log(message=f"Recieved note {__ITEM_ID}",section="VkNote",name="message")
        if __ITEM_ID == None:
            __ITEM_ID  = f"{NOTE.get("owner_id")}_{NOTE.get("id")}"
            __SOURCE   = f"vk:note{__ITEM_ID}"
        else:
            __SOURCE = f"vk:note{__ITEM_ID}"
        
        NOTE["site"] = self.passed_params.get("vk_path")
        __NOTE_INDEX = NOTE.copy()
        __NOTE_INDEX["text"] = utils.proc_strtr(__NOTE_INDEX.get("text"), self.passed_params.get("indexation_text_cut"))
        __indexation = utils.clearJson(__NOTE_INDEX)
        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "indexation_content": __indexation,
            "entity_internal_content": NOTE,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        return {
            "entities": [
                ENTITY
            ]
        }
