from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import VkApi, Path, os, logger, download_manager, utils
from resources.Exceptions import NotFoundException

# Downloads photo from vk.com using api.
class VkVideo(VkTemplate):
    name = 'VkVideo'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
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

    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("video.get", {"videos": item_id, "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/video1_1
        __VIDEO_RES = None
        __VIDEO_ID  = self.passed_params.get("item_id")
        __VIDEO_OBJECT = None
        if self.passed_params.get("__json_info") == None:
            __VIDEO_RES = await self.__recieveById(__VIDEO_ID)
            try:
                if __VIDEO_RES.get("items") != None:
                    __VIDEO_OBJECT = __VIDEO_RES.get("items")[0]
                    __VIDEO_ID  = f"{__VIDEO_OBJECT.get("owner_id")}_{__VIDEO_OBJECT.get("id")}"
                else:
                    __VIDEO_OBJECT = __VIDEO_RES[0]
            except:
                __VIDEO_OBJECT = None
        else:
            __VIDEO_RES = self.passed_params.get("__json_info")
            try:
                __VIDEO_OBJECT = __VIDEO_RES
            except Exception:
                __VIDEO_OBJECT = None
        
        if __VIDEO_OBJECT == None:
            raise NotFoundException("video not found")
        
        # Downloading
        VIDEO_NAME = __VIDEO_OBJECT.get("title")
        ORIGINAL_NAME = f"{utils.validName(VIDEO_NAME)}.mp4"
        SAVE_PATH = Path(os.path.join(self.temp_dir, ORIGINAL_NAME))
        logger.log(message=f"Recieved video {__VIDEO_ID}",section="VK",name="message")
        
        IS_DIRECT = __VIDEO_OBJECT.get("platform", None) == None
        if IS_DIRECT:
            if self.passed_params.get("download_file") == True:
                if __VIDEO_OBJECT.get("files") != None:
                    # TODO select another quality
                    VIDEO_URL = __VIDEO_OBJECT.get("files").get("mp4_480")
                    # TODO hls download
                    if ".m3u8" not in VIDEO_URL:
                        logger.log(message=f"Video {__VIDEO_ID} contains direct mp4; downloading",section="VKVideo",name="message")
                        HTTP_REQUEST = await download_manager.addDownload(end=VIDEO_URL,dir=SAVE_PATH)
                    else:
                        logger.log(message=f"Video {__VIDEO_ID} has HLS; downloading",section="VKVideo",name="message")
            else:
                logger.log(message=f"Do not downloading video {__VIDEO_ID} cuz download_file=0",section="VKVideo",name="message")
        else:
            logger.log(message=f"Video {__VIDEO_ID} is from another platform. Do not downloading file.",section="VK",name="message")

        __VIDEO_OBJECT["site"] = self.passed_params.get("vk_path")

        FILE = None
        if IS_DIRECT and self.passed_params.get("download_file"):
            FILE = self._fileFromJson({
                "extension": "mp4",
                "upload_name": ORIGINAL_NAME,
                "filesize": SAVE_PATH.stat().st_size,
            })
        
        ENTITY = self._entityFromJson({
            "suggested_name": VIDEO_NAME,
            "source": "vk:video"+str(__VIDEO_ID),
            "internal_content": __VIDEO_OBJECT,
            "file": FILE,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        return {
            "entities": [
                ENTITY
            ]
        }
