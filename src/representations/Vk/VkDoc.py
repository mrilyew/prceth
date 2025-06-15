from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from representations.Vk.BaseVk import BaseVkItemId
from utils.MainUtils import valid_name
from app.App import logger
from pathlib import Path
import os

class VkDoc(BaseVkItemId):
    def declare():
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids_str = i.get('item_id')
            items_ids = items_ids_str.split(",")

            response = await self.vkapi.call("docs.getById", {"docs": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, link_entities):
            self.outer._insertVkLink(item, self.buffer.get('args').get('vk_path'))

            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            private_url = item.get("private_url")
            is_do_unlisted = self.buffer.get('args').get("unlisted") == 1

            logger.log(message=f"Recieved document {item_id}",section="VkEntity",kind="message")

            item_ext = item.get("ext")
            item_title = item.get("title")
            file_name = valid_name(item_title + "." + item_ext)
            item_url = item.get("url")
            item_filesize = item.get("size", 0)

            if self.buffer.get('args').get("download") == True:
                main_su = self.storageUnit()
                temp_dir = main_su.temp_dir

                save_path = Path(os.path.join(temp_dir, file_name))

                await download_manager.addDownload(end=item_url,dir=save_path)

                file_stats = save_path.stat()

                main_su.write_data({
                    "extension": item_ext,
                    "upload_name": file_name,
                    "filesize": file_stats.st_size,
                })

                logger.log(message=f"Download file for doc {item_id}",section="VkEntity",kind="success")

            cu = self.contentUnit({
                "main_su": main_su,
                "name": item_title,
                "source": {
                    'type': 'vk',
                    'vk_type': 'doc',
                    'content': item_id
                },
                "content": item,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get("date"),
            })

            link_entities.append(cu)
