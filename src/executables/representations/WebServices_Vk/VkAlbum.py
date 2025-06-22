from executables.representations.WebServices_Vk import BaseVkItemId
from executables.representations.WebServices_Vk.VkPhoto import VkPhoto
from app.App import logger
from db.DbInsert import db_insert

class VkAlbum(BaseVkItemId):
    async def getPhotos(self, vkapi, offset, count, rev = False, download = False):
        hd = self.hydrated.json_content

        photos = await vkapi.call('photos.get', {
            "owner_id": hd.get('owner_id'),
            "album_id": hd.get('id'),
            "offset": offset,
            "count": count,
            "rev": int(rev), 
            "extended": 1,
            "photo_sizes": 1,
        })

        return await VkPhoto.extract({
            'object': photos,
            'download': download
        })

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            item_id_str = i.get('ids')
            items_ids = item_id_str.split(",")

            owner_id = None
            album_ids = []

            for item in items_ids:
                spl = item.split('_')
                owner_id = spl[0]

                match(spl[1]):
                    case '0':
                        album_ids.append('profile')
                    case '00':
                        album_ids.append('wall')
                    case '000':
                        album_ids.append('saved')
                    case _:
                        album_ids.append(spl[1])

            response = await self.vkapi.call("photos.getAlbums", {"owner_id": owner_id, "album_ids": ",".join(album_ids), "need_covers": 1, "photo_sizes": 1})

            return response

        async def item(self, item, list_to_add):
            is_do_unlisted = self.args.get("unlisted") == 1
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            name = item.get('title')

            self.outer._insertVkLink(item, self.args.get('vk_path'))

            logger.log(message=f"Recieved album {item_id}",section="Vk!Album",kind=logger.KIND_MESSAGE)

            alb = db_insert.contentFromJson({
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
