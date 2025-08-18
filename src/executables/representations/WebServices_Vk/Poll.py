from executables.representations.WebServices_Vk import BaseVkItemId
from declarable.ArgumentsTypes import BooleanArgument
from pathlib import Path
from app.App import logger
from submodules.Web.DownloadManager import download_manager
import os

class Poll(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download_bg"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            output = {
                'items': [],
                'profiles': [],
                'groups': []
            }

            for _id in i.get('ids').split(","):
                ids = _id.split('_')
                response = await self.vkapi.call("polls.getById", {"owner_id": ids[0], "poll_id": ids[1], "extended": 1})

                output.update(response)

            return response

        async def item(self, item, list_to_add):
            download_bg = self.args.get("download_bg")
            item_id = f"{item.get('owner_id')}_{item.get('id')}"

            self.outer._insertVkLink(item, self.args.get('vk_path'))

            out = self.ContentUnit()
            out.display_name = item.get("question")
            out.declared_created_at = item.get("date")
            out.source = {
                'type': 'vk',
                'vk_type': 'poll',
                'content': item_id
            }
            out.content = item
            out.unlisted = self.args.get("unlisted") == 1

            logger.log(message=f"Recieved poll {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            if download_bg == True:
                bg_su = self.StorageUnit()
                poll_bg = item.get("photo")

                try:
                    assert poll_bg != None

                    photo_sizes = sorted(poll_bg.get("images"), key=lambda x: (x['width'] is not None, x['width']), reverse=True)
                    optimal_size = photo_sizes[0]
                    assert optimal_size != None

                    save_path = Path(os.path.join(bg_su.temp_dir, f"poll{item_id}.jpg"))

                    await download_manager.addDownload(end=optimal_size.get("url"),dir=save_path)

                    bg_su.set_main_path(save_path)
                    out.add_link(bg_su)

                    item["relative_photo"] = bg_su.sign()

                    logger.log(message=f"Downloaded poll {item_id} background",section="Vk",kind=logger.KIND_SUCCESS)
                except Exception as _e:
                    logger.logException(_e,section="Vk",prefix="Error downloading poll bg: ")

            list_to_add.append(out)
