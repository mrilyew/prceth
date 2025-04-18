from resources.Globals import VkApi, utils, logger
from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkNote(VkTemplate):
    name = 'VkNote'
    category = 'Vk'
    hidden = True

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

    async def __recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        __item_id = item_ids[0].split("_")

        return await __vkapi.call("notes.getById", {"owner_id": __item_id[0], "note_id": __item_id[1]})
    
    async def run(self, args):
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        notes = None

        if self.passed_params.get("__json_info") == None:
            try:
                notes = await self.__recieveById(item_ids)
            except:
                notes = None
        else:
            try:
                notes = self.passed_params.get("__json_info")
            except:
                pass
        
        if type(notes) == dict:
            notes = [notes]
        
        if notes == None or len(notes) < 1:
            raise NotFoundException("note not found")

        __entities_list = []
        for note in notes:
            __ITEM_ID  = f"{note.get('owner_id')}_{note.get('id')}"
            __SOURCE   = f"vk:note{__ITEM_ID}"

            logger.log(message=f"Recieved note {__ITEM_ID}",section="VkAttachments",name="message")

            note["site"] = self.passed_params.get("vk_path")
            __note_index = note.copy()
            __note_index["text"] = utils.proc_strtr(__note_index.get("text"), self.passed_params.get("indexation_text_cut"))

            ENTITY = self._entityFromJson({
                "source": __SOURCE,
                "indexation_content": __note_index,
                "internal_content": note,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "suggested_name": utils.proc_strtr(note.get("title"), 1000),
                "declared_created_at": note.get("date"),
            })
            __entities_list.append(ENTITY)

        return {
            "entities": __entities_list
        }
