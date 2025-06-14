from representations.Vk.BaseVk import BaseVk, VkExtractStrategy
from declarable.ArgumentsTypes import ObjectArgument, IntArgument, StringArgument, BooleanArgument, CsvArgument
from app.App import logger

class VkAlbum(BaseVk):
    category = 'Vk'

    def declare():
        params = {}
        params["object"] = ObjectArgument({})
        params["item_id"] = StringArgument({})

        return params

    class Extractor(VkExtractStrategy):
        def extractWheel(self, i = {}):
            if i.get('object') != None:
                return 'extractByObject'
            elif 'item_id' in i:
                return 'extractById'

        async def extractByObject(self, i = {}):
            objects = i.get("object")

            items = objects

            return await self.gatherList(items, self.item)

        async def extractById(self, i = {}):
            items_ids_string = i.get('item_id')
            items_ids = items_ids_string.split(",")
            owner_id = None
            item_second_ids = []

            for item in items_ids:
                owner_id = item[0]

                item_second_ids.append(item[1])

            response = await self.vkapi.call("photos.getAlbums", {"owner_id": owner_id, "album_ids": ",".join(item_second_ids), "need_covers": 1, "photo_sizes": 1})

            items = response.get('items')

            return await self.gatherTasksByTemplate(items, self.item)

        async def item(self, item, list_to_add):
            is_do_unlisted = self.buffer.get('args').get("unlisted") == 1
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            name = f"Album \"{item.get('title')}\""

            self.outer._insertVkLink(item, self.buffer.get('args').get('vk_path'))

            logger.log(message=f"Recieved album {item_id}",section="VkEntity",kind="message")

            alb = self.contentUnit({
                "source": {
                    'type': 'vk',
                    'vk_type': "album",
                    'content': item_id
                },
                "content": item,
                "unlisted": is_do_unlisted,
                "name": name,
                "description": item.get("description"),
                "declared_created_at": item.get("date"),
            })

            list_to_add.append(alb)
