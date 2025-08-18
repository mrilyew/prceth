from executables.representations.WebServices_Vk import BaseVkItemId
from app.App import logger
from utils.MainUtils import proc_strtr

class Note(BaseVkItemId):
    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            output = {
                'items': []
            }

            for _id in i.get('ids'):
                ids = _id.split('_')
                item = await self.vkapi.call("notes.getById", {"owner_id": ids[0], "note_id": ids[1]})

                output.get("items").append(item)

            return output

        async def item(self, item, list_to_add):
            item_id  = f"{item.get('owner_id')}_{item.get('id')}"
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            out = self.ContentUnit()
            out.content = item
            out.display_name = proc_strtr(item.get("title"), 100)
            out.declared_created_at = item.get("date")
            out.unlisted = self.args.get("unlisted") == 1
            out.source = {
                'type': 'vk',
                'vk_type': 'note',
                'content': item_id
            }

            logger.log(message=f"Recieved note {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            list_to_add.append(out)
