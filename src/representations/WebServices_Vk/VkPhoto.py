from submodules.Web.DownloadManager import download_manager
from representations.WebServices_Vk.BaseVk import BaseVkItemId
from declarable.ArgumentsTypes import BooleanArgument
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

            logger.log(message=f"Recieved photo {item_id}",section="VkEntity!Photo",kind="message")
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            if item.get('orig_photo') != None:
                download_url = item.get('orig_photo').get("url")
            else:
                if item.get('url') != None:
                    download_url = item.get('url')
                else:
                    try:
                        __photo_sizes = sorted(item.get('sizes'), key=lambda x: (x['width'] is None, x['width']), reverse=True)
                        __optimal_size = __photo_sizes[0]
                        # For old photos without sizes.
                        if __optimal_size.get('height') == 0:
                            __optimal_size = item.get('sizes')[-1]
                        
                        download_url = __optimal_size.get('url')
                    except Exception as ___e:
                        logger.logException(___e, section="VkEntity!Photo")

            if self.args.get('download') == True:
                original_name = f"photo_{item_id}_{item.get('date')}.jpg"

                item_su = self.storageUnit()
                temp_dir = item_su.temp_dir

                try:
                    save_path = Path(os.path.join(temp_dir, original_name))

                    await download_manager.addDownload(end = download_url, dir = save_path)

                    file_stats = save_path.stat()

                    item_su.write_data({
                        "extension": "jpg",
                        "upload_name": original_name,
                        "filesize": file_stats.st_size,
                    })

                    logger.log(message=f"Downloaded photo {item_id}",section="VkEntity!Photo",kind="success")
                except FileNotFoundError as _ea:
                    logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VkEntity",kind="error")

            __cu = self.contentUnit({
                "main_su": item_su,
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
