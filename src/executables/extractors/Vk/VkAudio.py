from executables.extractors.Vk.VkBase import VkBase
from resources.Globals import os, download_manager, VkApi, Path, asyncio, utils, logger, media_utils
from resources.Exceptions import NotFoundException, LibNotInstalledException

class VkAudio(VkBase):
    name = 'VkAudio'
    category = 'Vk'
    docs = {
        "description": {
            "name": {
                "ru": "VK Аудиозапись",
                "en": "VK Audio"
            },
            "definition": {
                "ru": "Аудиофайл из vk",
                "en": "Audio from vk"
            }
        },
    }
    file_containment = {
        "files_count": "1",
        "files_extensions": ["mp3"]
    }

    def declare():
        params = {}
        params["item_id"] = {
            "docs": {
                "definition": {
                    "ru": "ID аудиозаписи",
                    "en": "ID of audio",
                }
            },
            "type": "string",
        }
        params["__json_info"] = {
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }
        params["download_file"] = {
            "docs": {
                "definition": {
                    "ru": "Скачивать ли аудиофайл (через yt-dlp)",
                    "en": "Do download audio file (via yt-dlp)",
                }
            },
            "type": "bool",
            "default": True
        }

        return params

    async def recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("audio.getById", {"audios": ",".join(item_ids), "extended": 1})

    async def run(self, args):
        __audio_response = None
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        if self.passed_params.get("__json_info") == None:
            try:
                __audio_response = await self.recieveById(item_ids)
                if __audio_response.get("items") != None:
                    __audio_response = __audio_response.get("items")
            except:
                pass
        else:
            try:
                __audio_response = self.passed_params.get("__json_info")
                if type(__audio_response) == dict:
                    __audio_response = [__audio_response]
            except:
                __audio_response = None

        if __audio_response == None or len(__audio_response) < 1:
            raise NotFoundException("audio not found")
        
        __entities_list = []
        __tasks = []
        for item in __audio_response:
            __task = asyncio.create_task(self.__item(item, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        item["site"] = self.passed_params.get("vk_path")

        __ITEM_ID = f"{item.get('owner_id')}_{item.get('id')}"
        __SOURCE  = f"vk:audio{__ITEM_ID}"

        logger.log(message=f"Recieved audio {__ITEM_ID}",section="VkAttachments",name="message")

        FILE = None
        ___OUT_EXT  = "mp3"
        ___OUT_SIZE = 0

        AUDIO_NAME = f"{item.get('artist')} — {item.get('title')}"
        AUDIO_UPLOAD_NAME = utils.validName(AUDIO_NAME) + f".{___OUT_EXT}"

        if self.passed_params.get("download_file") == True:
            TEMP_DIR = self.allocateTemp()
            ___SAVE_PATH = Path(os.path.join(TEMP_DIR, AUDIO_UPLOAD_NAME))

            if item.get("url") == None:
                logger.log(message=f"Audio {__ITEM_ID} does not contains url to file",section="VkAudio",name="error")
            else:
                # Todo HLS
                if ".m3u8" in item.get("url"):
                    from submodules.Media.YtDlpWrapper import YtDlpWrapper

                    if media_utils.isFFMPEGInstalled() == False:
                        raise LibNotInstalledException("ffmpeg is not installed")

                    logger.log(message=f"Found .m3u8 of audio {__ITEM_ID}",section="VkAudio",name="message")
                    params = {"outtmpl": str(___SAVE_PATH)}
                    with YtDlpWrapper(params).ydl as ydl:
                        info = ydl.extract_info(item.get("url"), download=True)

                    FILE = self._fileFromJson({
                        "extension": ___OUT_EXT,
                        "upload_name": AUDIO_UPLOAD_NAME,
                        "filesize": ___SAVE_PATH.stat().st_size,
                    })
                else:
                    logger.log(message=f"Downloading raw .mp3 of audio {__ITEM_ID}",section="VkAudio",name="message")

                    DOWNLOAD_URL = item.get("url")
                    HTTP_REQUEST = await download_manager.addDownload(end=DOWNLOAD_URL,dir=___SAVE_PATH)
                    ___OUT_SIZE = ___SAVE_PATH.stat().st_size

                    FILE = self._fileFromJson({
                        "extension": ___OUT_EXT,
                        "upload_name": AUDIO_UPLOAD_NAME,
                        "filesize": ___OUT_SIZE,
                    })

        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "internal_content": item,
            "suggested_name": AUDIO_NAME,
            "file": FILE,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
        })
        link_entities.append(ENTITY)
