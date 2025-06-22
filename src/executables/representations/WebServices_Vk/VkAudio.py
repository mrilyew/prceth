from executables.representations.WebServices_Vk import BaseVkItemId
from resources.Exceptions import LibNotInstalledException
from declarable.ArgumentsTypes import BooleanArgument
from submodules.Web.DownloadManager import download_manager
from pathlib import Path
from app.App import logger
from utils.MainUtils import valid_name
from utils.MediaUtils import is_ffmpeg_installed
from db.DbInsert import db_insert
import os

class VkAudio(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            item_id_str = i.get('ids')
            items_ids = item_id_str.split(",")

            resp = await self.vkapi.call("audio.getById", {"audios": ",".join(items_ids), "extended": 1})

            return resp

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))
            is_do_unlisted = self.args.get("unlisted") == 1
            item_id = f"{item.get('owner_id')}_{item.get('id')}"

            logger.log(message=f"Recieved audio {item_id}",section="Vk!Audio",kind="message")

            main_su = None

            audio_name = f"{item.get('artist')} — {item.get('title')}"
            audio_save_name = valid_name(audio_name) + f".mp3"
            save_path = None

            if self.args.get("download") == True:
                main_su = db_insert.storageUnit()
                temp_dir = main_su.temp_dir

                save_path = Path(os.path.join(temp_dir, audio_save_name))

                if item.get("url") == None:
                    logger.log(message=f"Audio {item_id} does not contains url to file",section="Vk!Audio",kind="error")
                else:
                    download_url = item.get("url")

                    if ".m3u8" in download_url:
                        from submodules.Media.YtDlpWrapper import YtDlpWrapper

                        if is_ffmpeg_installed() == False:
                            raise LibNotInstalledException("ffmpeg is not installed")

                        logger.log(message=f"Found .m3u8 of audio {item_id}",section="Vk!Audio",kind="message")

                        with YtDlpWrapper({"outtmpl": str(save_path)}).ydl as ydl:
                            info = ydl.extract_info(download_url, download=True)
                    else:
                        logger.log(message=f"Downloading raw .mp3 of audio {item_id}",section="Vk!Audio",kind="message")

                        await download_manager.addDownload(end=download_url,dir=save_path)

                main_su.set_main_file(save_path)

            cu = db_insert.contentFromJson({
                "source": {
                    'type': 'vk',
                    'vk_type': 'audio',
                    'content': item_id,
                },
                "content": item,
                "name": audio_name,
                "links": [main_su],
                "link_main": 0,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get("date"),
            })

            list_to_add.append(cu)
