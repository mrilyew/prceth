from resources.Globals import VkApi, utils, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkNote(VkTemplate):
    name = 'VkNote'
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
        params["indexation_text_cut"] = {
            "desc_key": "-",
            "type": "int",
            "hidden": True,
            "default": 699,
        }

        return params

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
        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "internal_content": NOTE,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        return {
            "entities": [
                ENTITY
            ]
        }
