from executables.extractors.Vk.VkBase import VkBase
from resources.Globals import VkApi, Path, os, logger, download_manager, utils, asyncio, media_utils
from resources.Exceptions import NotFoundException, LibNotInstalledException

# Downloads photo from vk.com using api.
class VkVideo(VkBase):
    name = 'VkVideo'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["quality"] = {
            "desc_key": "-",
            "type": "string",
            "default": "max",
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": False,
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }

        return params

    async def recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("video.get", {"videos": ",".join(item_ids), "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/video1_1
        __item_ids  = self.passed_params.get("item_id")
        item_ids    = __item_ids.split(",")
        video_items = None

        if self.passed_params.get("__json_info") == None:
            videos_response = await self.recieveById(item_ids)
            try:
                if videos_response.get("items") != None:
                    video_items = videos_response.get("items")
                else:
                    video_items = videos_response
            except:
                video_items = None
        else:
            video_items = self.passed_params.get("__json_info")
            if type(video_items) == dict:
                video_items = [video_items]
        
        if video_items == None or len(video_items) < 1:
            raise NotFoundException("video not found")
        
        __entities_list = []
        __tasks = []
        for video in video_items:
            __task = asyncio.create_task(self.__item(video, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        FILE = None
        item["site"] = self.passed_params.get("vk_path")

        VIDEO_ID  = f"{item.get('owner_id')}_{item.get('id')}"
        VIDEO_NAME = item.get("title")
        ORIGINAL_NAME = f"{utils.validName(VIDEO_NAME)}.mp4"
        VIDEO_PAGE_URL = f"https://vkvideo.ru/video{VIDEO_ID}"

        logger.log(message=f"Recieved video {VIDEO_ID}",section="VkAttachments",name="message")

        IS_DIRECT = item.get("platform") == None
        if IS_DIRECT:
            try:
                if self.passed_params.get("download_file") == True:
                    QUALITY = self.passed_params.get("quality")
                    TEMP_DIR = self.allocateTemp()
                    SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))

                    try:
                        if item.get("files") != None:
                            FILES_LIST = item.get("files")
                            MAX_QUALITY = utils.findHighestInDict(FILES_LIST, "mp4_")
                            VIDEO_URL = None
                            HLS_URL = FILES_LIST.get("hls")
                            if QUALITY == "max":
                                VIDEO_URL = FILES_LIST.get(f"mp4_{MAX_QUALITY}")
                            else:
                                VIDEO_URL = FILES_LIST.get(f"mp4_{QUALITY}")

                            if VIDEO_URL == None:
                                raise NotFoundException(f"Video {VIDEO_ID}: not found mp4")

                            if "srcIp=" not in VIDEO_URL:
                                logger.log(message=f"Video {VIDEO_ID} contains direct mp4; downloading",section="VkAttachments",name="message")
                                HTTP_REQUEST = await download_manager.addDownload(end=VIDEO_URL,dir=SAVE_PATH)
                            else:
                                raise Exception("-")
                        else:
                            raise NotFoundException(f"Video {VIDEO_ID} doesn't has files")
                    except:
                        from submodules.Media.YtDlpWrapper import YtDlpWrapper
                        
                        if media_utils.isFFMPEGInstalled() == False:
                            raise LibNotInstalledException("ffmpeg is not installed")

                        logger.log(message=f"Making direct download via yt-dlp...",section="VkAttachments",name="message")
                        params = {"outtmpl": str(SAVE_PATH)}
                        if QUALITY != "max":
                            params["format"] = f"url{QUALITY}"

                        with YtDlpWrapper(params).ydl as ydl:
                            info = ydl.extract_info(VIDEO_PAGE_URL, download=True)

                    FILE = self._fileFromJson({
                        "extension": "mp4",
                        "upload_name": ORIGINAL_NAME,
                        "filesize": SAVE_PATH.stat().st_size,
                    })
                    item["relative_file"] = f"__lcms|file_{FILE.id}"
            except LibNotInstalledException as _libe:
                raise _libe
            except Exception as __e:
                logger.logException(__e, section="VkAttachments",silent=False)
        else:
            logger.log(message=f"Video {VIDEO_ID} is from another platform ({item.get("platform")})",section="VkAttachments",name="message")
        
        ENTITY = self._entityFromJson({
            "suggested_name": VIDEO_NAME,
            "source": "vk:video"+str(VIDEO_ID),
            "internal_content": item,
            "file": FILE,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
        })
        link_entities.append(ENTITY)
