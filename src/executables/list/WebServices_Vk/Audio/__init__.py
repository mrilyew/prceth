from executables.list.WebServices_Vk import BaseVkItemId
from resources.Exceptions import LibNotInstalledException
from declarable.Arguments import BooleanArgument
from submodules.Web.DownloadManager import download_manager
from pathlib import Path
from app.App import logger
from utils.MainUtils import valid_name
from utils.MediaUtils import is_ffmpeg_installed
import os

class Implementation(BaseVkItemId):
    required_modules = ["yt-dlp"]

    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')
            response = await self.vkapi.call("audio.getById", {"audios": ",".join(items_ids), "extended": 1})

            return response

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            do_download = self.args.get("download")
            audio_name = f"{item.get('artist')} — {item.get('title')}"
            audio_save_name = valid_name(audio_name) + f".mp3"
            item_id = f"{item.get('owner_id')}_{item.get('id')}"

            out = self.ContentUnit()
            out.content = item
            out.declared_created_at = item.get("date")
            out.source = {
                'type': 'vk',
                'vk_type': 'audio',
                'content': item_id,
            }

            if do_download == True:
                su = self.StorageUnit()
                save_path = Path(os.path.join(su.temp_dir, audio_save_name))

                if item.get("url") == None:
                    logger.log(message=f"Audio {item_id} does not contains url to file",section="Vk",kind=logger.KIND_ERROR)
                else:
                    download_url = item.get("url")

                    if ".m3u8" in download_url:
                        from submodules.Media.YtDlpWrapper import YtDlpWrapper

                        if is_ffmpeg_installed() == False:
                            raise LibNotInstalledException("ffmpeg is not installed")

                        logger.log(message=f"Found .m3u8 of audio {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

                        with YtDlpWrapper({"outtmpl": str(save_path)}).ydl as ydl:
                            info = ydl.extract_info(download_url, download=True)
                    else:
                        logger.log(message=f"Downloading raw .mp3 of audio {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

                        await download_manager.addDownload(end=download_url,dir=save_path)

                su.set_main_file(save_path)
                logger.log(message=f"Downloaded .mp3 of audio {item_id} ({out.uuid})",section="Vk",kind=logger.KIND_MESSAGE)

                out.add_link(su)
                out.set_common_link(su)

            logger.log(message=f"Recieved audio {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            list_to_add.append(out)
