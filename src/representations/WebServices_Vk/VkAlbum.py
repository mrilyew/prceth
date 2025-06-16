from representations.WebServices_Vk import BaseVkItemId
from app.App import logger

class VkAlbum(BaseVkItemId):
    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            item_id_str = i.get('ids')
            items_ids = item_id_str.split(",")

            owner_id = None
            album_ids = []

            for item in items_ids:
                spl = item.split('_')
                owner_id = spl[0]

                album_ids.append(spl[1])

            response = await self.vkapi.call("photos.getAlbums", {"owner_id": owner_id, "album_ids": ",".join(album_ids), "need_covers": 1, "photo_sizes": 1})

            return response

        async def item(self, item, list_to_add):
            is_do_unlisted = self.args.get("unlisted") == 1
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            name = f"Album \"{item.get('title')}\""

            self.outer._insertVkLink(item, self.args.get('vk_path'))

            logger.log(message=f"Recieved album {item_id}",section="Vk!Album",kind="message")

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
