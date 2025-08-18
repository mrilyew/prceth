from executables.representations.WebServices_Vk import BaseVkItemId
from executables.representations.WebServices_Vk.Photo import Photo
from app.App import logger

class Album(BaseVkItemId):
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

        return await Photo.extract({
            'object': photos,
            'download': download
        })

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')

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
            self.outer._insertVkLink(out.content, self.args.get('vk_path'))

            item_id = f"{item.get('owner_id')}_{item.get('id')}"

            out = self.ContentUnit()
            out.display_name = item.get('title')
            out.description = item.get("description")
            out.source = {
                'type': 'vk',
                'vk_type': "album",
                'content': item_id
            }
            out.content = item
            out.unlisted = self.args.get("unlisted") == 1
            out.declared_created_at = item.get("date")

            logger.log(message=f"Recieved album {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            list_to_add.append(out)
