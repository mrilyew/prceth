from representations.Vk.BaseVk import BaseVkByItemId
from declarable.ArgumentsTypes import ObjectArgument, IntArgument, StringArgument, BooleanArgument, CsvArgument
from app.App import logger

class VkAlbum(BaseVkByItemId):
    category = 'Vk'
    docs = {
        "name": '__vk_album',
        "definition": '__vk_album'
    }

    def declare():
        params = {}
        params["object"] = ObjectArgument({})
        params["item_id"] = StringArgument({})

        return params

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

    async def getList(self, i = {}):
        owner_id = i.get('owner_id')

        pass

    async def getPhotos(self, i = {}):
        pass

    async def item(self, item, list_to_add):
        item_id = f"{item.get('owner_id')}_{item.get('id')}"
        source = {
            'type': 'vk',
            'vk_type': "album",
            'content': item_id
        }
        name = f"Album \"{item.get('title')}\""

        self._insertVkLink(item, self.buffer.get('args').get('vk_path'))

        logger.log(message=f"Recieved album {item_id}",section="VkCollection",name="message")

        alb = self.new_cu({
            "source": source,
            "content": item,
            "unlisted": True,
            "name": name,
            "description": item.get("description"),
            "declared_created_at": item.get("date"),
        })

        list_to_add.append(alb)
