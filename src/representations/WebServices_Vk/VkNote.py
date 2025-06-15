from representations.WebServices_Vk.BaseVk import BaseVkItemId
from app.App import logger
from utils.MainUtils import proc_strtr

class VkNote(BaseVkItemId):
    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            item_id = i.get('ids')
            item_ids = item_id.split(',')
            final_response = {
                'items': []
            }

            assert len(item_ids) < 3, 'bro too many'

            for id in item_ids:
                spl = id.split('_')
                item = await self.vkapi.call("notes.getById", {"owner_id": spl[0], "note_id": spl[1]})

                final_response['items'].append(item)

            return final_response

        async def item(self, item, list_to_add):
            item_id  = f"{item.get('owner_id')}_{item.get('id')}"
            is_do_unlisted = self.buffer.get('args').get("unlisted") == 1

            self.outer._insertVkLink(item, self.buffer.get('args').get('vk_path'))

            logger.log(message=f"Recieved note {item_id}",section="VkEntity",kind="message")

            cu = self.contentUnit({
                "source": {
                    'type': 'vk',
                    'vk_type': 'note',
                    'content': item_id
                },
                "content": item,
                "unlisted": is_do_unlisted,
                "name": proc_strtr(item.get("title"), 100),
                "declared_created_at": item.get("date"),
            })

            list_to_add.append(cu)
