from executables.representations.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from db.DbInsert import db_insert
from app.App import logger
from pathlib import Path
import os

class VkPhoto(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    @classmethod
    async def countByUser(cls, vkapi, owner_id):
        resp = await vkapi.call('photos.getAll', {"owner_id": owner_id, "count": 1})

        return resp.get('count')

    @classmethod
    async def byUser(cls, vkapi, owner_id, offset, count, rev = False, download = False):
        photos = await vkapi.call('photos.getAll', {
            "owner_id": owner_id,
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
            items_ids_str = i.get('ids')
            items_ids = items_ids_str.split(",")

            response = await self.vkapi.call("photos.getById", {"photos": (",".join(items_ids)), "photo_sizes": 1, "extended": 1})

            return response

        async def item(self, item, list_to_add):
            download_url = ""
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            item_su = None
            is_do_unlisted = self.args.get("unlisted") == 1

            # So, downloading photo

            logger.log(message=f"Recieved photo {item_id}",section="Vk!Photo",kind="message")
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            if item.get('orig_photo') != None:
                download_url = item.get('orig_photo').get("url")
            else:
                if item.get('url') != None:
                    download_url = item.get('url')
                else:
                    try:
                        __photo_sizes = sorted(item.get('sizes'), key=lambda x: (x['width'] is not None, x['width']), reverse=True)
                        __optimal_size = __photo_sizes[0]
                        # For old photos without sizes.
                        if __optimal_size.get('height') == 0:
                            __optimal_size = item.get('sizes')[-1]
                        
                        download_url = __optimal_size.get('url')
                    except Exception as ___e:
                        logger.logException(___e, section="Vk!Photo")

            if self.args.get('download') == True:
                original_name = f"photo_{item_id}_{item.get('date')}.jpg"

                item_su = db_insert.storageUnit()
                temp_dir = item_su.temp_dir

                try:
                    save_path = Path(os.path.join(temp_dir, original_name))

                    await download_manager.addDownload(end = download_url, dir = save_path)

                    item_su.set_main_file(save_path)

                    logger.log(message=f"Downloaded photo {item_id}",section="Vk!Photo",kind="success")
                except FileNotFoundError as _ea:
                    logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="Vk!Photo",kind="error")

            __cu = db_insert.contentFromJson({
                "links": [item_su],
                "link_main": 0,
                "name": f"VK Photo {str(item_id)}",
                "source": {
                    "type": 'vk',
                    'vk_type': 'photo',
                    'content': item_id
                },
                "content": item,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get('date'),
            })

            list_to_add.append(__cu)
