from executables.representations.WebServices_Vk import BaseVkItemId
from declarable.ArgumentsTypes import StringArgument, BooleanArgument
from app.App import logger
from pathlib import Path
from utils.MainUtils import valid_name
from utils.MediaUtils import find_highest_in_dict
from submodules.Web.DownloadManager import download_manager
from resources.Exceptions import LibNotInstalledException
from db.DbInsert import db_insert
import os

class Video(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download"] = BooleanArgument({
            "default": True
        })
        params["quality"] = StringArgument({
            "default": "max",
        })
        params["page_domain"] = StringArgument({
            "default": "https://vkvideo.ru/video",
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')

            response = await self.vkapi.call("video.get", {"videos": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            is_do_download = self.args.get("download") == True
            is_do_unlisted = self.args.get("unlisted") == 1
            quality = self.args.get("quality")
            page_domain = self.args.get('page_domain', '')

            storage_unit = None
            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            item_name = item.get("title")
            file_name = f"{valid_name(item_name)}.mp4"
            files_list = item.get("files")
            item_url = page_domain + f"{item_id}"
            is_direct = item.get("platform") == None

            logger.log(message=f"Recieved video {item_id}; download={is_do_download}",section="Vk!Video",kind=logger.KIND_MESSAGE)

            if is_do_download:
                if is_direct:
                    try:
                        from submodules.Media.YtDlpWrapper import YtDlpWrapper

                        storage_unit = db_insert.storageUnit()
                        temp_dir = storage_unit.temp_dir

                        save_path = Path(os.path.join(temp_dir, file_name))

                        assert files_list != None, 'no "files" found'

                        max_quality = find_highest_in_dict(files_list, "mp4_")
                        video_file_url = None

                        if quality == "max":
                            video_file_url = files_list.get(f"mp4_{max_quality}")
                        else:
                            video_file_url = files_list.get(f"mp4_{quality}")

                        async def _byPage():
                            logger.log(message=f"Making raw page download via yt-dlp",section="Vk!Video",kind=logger.KIND_MESSAGE)

                            ytd_params = {"outtmpl": str(save_path)}
                            if quality != "max":
                                ytd_params["format"] = f"url{quality}"

                            with YtDlpWrapper(ytd_params).ydl as ydl:
                                info = ydl.extract_info(item_url, download=True)

                        async def _byMp4():
                            logger.log(message=f"Video {item_id} contains direct mp4; downloading",section="Vk!Video",kind=logger.KIND_MESSAGE)

                            await download_manager.addDownload(end=video_file_url,dir=save_path)

                        async def _byHls():
                            logger.log(message=f"Making download via yt-dlp",section="Vk!Video",kind=logger.KIND_MESSAGE)

                            with YtDlpWrapper({"outtmpl": str(save_path)}).ydl as ydl:
                                info = ydl.extract_info(video_file_url, download=True)

                        if video_file_url == None:
                            await _byPage()

                        if "srcIp=" not in video_file_url:
                            await _byMp4()
                        else:
                            await _byPage()

                        storage_unit.set_main_file(save_path)
                    except LibNotInstalledException as _libe:
                        raise _libe
                    except AssertionError:
                        logger.log(message='Video files not found', section='Vk!Video', kind=logger.KIND_ERROR)
                    except Exception as __e:
                        logger.logException(__e, section="Vk",silent=False)
                else:
                    logger.log(message=f"Video {item_id} is from another platform ({item.get("platform")})",section="Vk!Video",kind=logger.KIND_MESSAGE)

            item.pop('files', None)
            item.pop('trailer', None)
            item.pop('stats_pixels', None)
            item.pop('ads', None)

            cu = db_insert.contentFromJson({
                "name": item_name,
                "source": {
                    'type': 'vk',
                    'vk_type': 'video',
                    'content': item_id
                },
                "content": item,
                "links": [storage_unit],
                "link_main": 0,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get("date"),
            })

            list_to_add.append(cu)
