from executables.representations.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from app.App import logger
from pathlib import Path
import os

class Photo(BaseVkItemId):
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

        return await Photo.extract({
            'object': photos,
            'download': download
        })

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            response = await self.vkapi.call("photos.getById", {"photos": (",".join(i.get('ids'))), "photo_sizes": 1, "extended": 1})

            return response

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            download_url = ""
            is_download = self.args.get('download')
            item_id = f"{item.get('owner_id')}_{item.get('id')}"

            out = self.ContentUnit()
            out.content = item
            out.display_name = f"Photo {str(item_id)}"
            out.unlisted = self.args.get("unlisted") == 1
            out.declared_created_at = item.get('date')
            out.source = {
                "type": 'vk',
                'vk_type': 'photo',
                'content': item_id
            }

            logger.log(message=f"Recieved photo {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            # So, downloading photo

            if item.get('orig_photo') != None:
                download_url = item.get('orig_photo').get("url")
            else:
                if item.get('url') != None:
                    download_url = item.get('url')
                else:
                    try:
                        __photo_sizes = sorted(item.get('sizes'), key=lambda x: (x['width'] is not None, x['width']), reverse=True)
                        __optimal_size = __photo_sizes[0]
                        # if size not available
                        if __optimal_size.get('height') == 0:
                            __optimal_size = item.get('sizes')[-1]

                        download_url = __optimal_size.get('url')
                    except Exception as ___e:
                        logger.logException(___e, section="Vk", prefix="Error downloading photo file: ")

            if is_download == True:
                main_su = self.StorageUnit()

                try:
                    save_path = Path(os.path.join(main_su.temp_dir, f"photo_{item_id}_{item.get('date')}.jpg"))

                    await download_manager.addDownload(end = download_url, dir = save_path)

                    main_su.set_main_file(save_path)
                    out.add_link(main_su)
                    out.set_common_link(main_su)

                    logger.log(message=f"Downloaded photo {item_id} (su_{main_su.uuid})",section="Vk",kind=logger.KIND_SUCCESS)
                except Exception as _ea:
                    logger.logException(_ea,section="Vk",prefix="Error downloading photo: ")

            list_to_add.append(out)
