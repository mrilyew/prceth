from executables.list.WebServices_Vk import BaseVkItemId
from app.App import logger
from declarable.Arguments import BooleanArgument
from utils.MediaUtils import find_highest_in_dict
from submodules.Web.DownloadManager import download_manager
from pathlib import Path
import os

class Implementation(BaseVkItemId):
    hidden = True

    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        def __response(self, i = {}):
            raise Exception('>:(')

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            is_do_download = self.args.get("download")
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            title = f"Graffiti {item_id.get('id')}"

            out = self.ContentUnit()
            out.display_name = title
            out.unlisted = self.args.get("unlisted") == 1
            out.content = item
            out.source = {
                'type': 'vk',
                'vk_type': 'graffiti',
                'content': item_id
            }

            logger.log(message=f"Recieved graffiti {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            if is_do_download:
                try:
                    max_size = find_highest_in_dict(item, "photo_")
                    main_su = self.StorageUnit()

                    download_url = item.get(f"photo_{max_size}")
                    save_path = Path(os.path.join(main_su.temp_dir, f"graffiti{item_id}.png"))

                    await download_manager.addDownload(end=download_url,dir=save_path)

                    main_su.set_main_file(save_path)
                    out.add_link(main_su)
                    out.set_common_link(main_su)

                    logger.log(message=f"Downloaded graffiti {item_id}",section="Vk",kind=logger.KIND_SUCCESS)
                except FileNotFoundError as _ea:
                    logger.log(message=f"Probaly broken photo file. Exception: {str(_ea)}",section="Vk",kind=logger.KIND_ERROR)

            list_to_add.append(out)
