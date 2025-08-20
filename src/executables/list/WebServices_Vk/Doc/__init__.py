from executables.list.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from utils.MainUtils import valid_name
from app.App import logger
from pathlib import Path
import os

class Implementation(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            return await self.vkapi.call("docs.getById", {"docs": (",".join(i.get('ids'))), "extended": 1})

        async def item(self, item, link_entities):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            item_title = item.get("title")
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            private_url = item.get("private_url")
            item_filesize = item.get("size", 0)
            item_url = item.get("url")
            item_ext = item.get("ext")

            out = self.ContentUnit()
            out.display_name = item_title
            out.source = {
                'type': 'vk',
                'vk_type': 'doc',
                'content': item_id
            }
            out.unlisted = self.args.get("unlisted") == 1
            out.declared_created_at = item.get("date")
            out.content = item

            logger.log(message=f"Recieved document {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            if self.args.get("download") == True:
                su = self.StorageUnit()
                save_path = Path(os.path.join(su.temp_dir, valid_name(item_title + "." + item_ext)))

                await download_manager.addDownload(end=item_url,dir=save_path)

                su.set_main_file(save_path)

                out.add_link(su)
                out.set_common_link(su)

                logger.log(message=f"Download file for doc {item_id}",section="Vk",kind=logger.KIND_SUCCESS)

            link_entities.append(out)
