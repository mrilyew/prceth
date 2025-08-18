from executables.representations.WebServices_Vk import BaseVkItemId
from declarable.ArgumentsTypes import BooleanArgument
from submodules.Web.DownloadManager import download_manager
from pathlib import Path
from app.App import logger
import os

class Link(BaseVkItemId):
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

            attached_photo = item.get("photo")
            do_download = self.args.get("download")

            out = self.ContentUnit()
            out.display_name = f"Vk Attached link"
            out.content = item
            out.source = {
                "type": 'url',
                "content": item.get('url')
            }
            out.unlisted = self.args.get('unlisted') == 1

            logger.log(message=f"Recieved attached link",section="Vk",kind=logger.KIND_MESSAGE)

            if do_download == True and attached_photo != None:
                photo_id = f"{attached_photo.get('owner_id')}_{attached_photo.get('id')}"

                try:
                    main_su = self.StorageUnit()

                    __photo_sizes = sorted(attached_photo.get("sizes"), key=lambda x: (x['width'] is not None, x['width']), reverse=True)
                    __optimal_size = __photo_sizes[0]
                    assert __optimal_size != None

                    save_path = Path(os.path.join(main_su.temp_dir, f"link_photo_{photo_id}.jpg"))

                    await download_manager.addDownload(end=__optimal_size.get("url"),dir=save_path)

                    main_su.set_main_file(save_path)
                    out.add_link(main_su)
                    out.set_common_link(main_su)

                    item['relative_photo'] = main_su.sign()

                    logger.log(message=f"Downloaded link's photo {photo_id}",section="Vk",kind=logger.KIND_SUCCESS)
                except Exception as _e:
                    logger.logException(_e,section="Vk",prefix="Could not download link preview: ")

            list_to_add.append(out)
