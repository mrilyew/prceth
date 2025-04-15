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

    async def __recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("video.get", {"videos": ",".join(item_ids), "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/video1_1
        __item_ids  = self.passed_params.get("item_id")
        item_ids    = __item_ids.split(",")
        video_items = None

        if self.passed_params.get("__json_info") == None:
            videos_response = await self.__recieveById(item_ids)
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
        for video in video_items:
            FILE = None
            video["site"] = self.passed_params.get("vk_path")

            VIDEO_ID  = f"{video.get("owner_id")}_{video.get("id")}"
            VIDEO_NAME = video.get("title")
            ORIGINAL_NAME = f"{utils.validName(VIDEO_NAME)}.mp4"

            logger.log(message=f"Recieved video {VIDEO_ID}",section="VkAttachments",name="message")
        
            IS_DIRECT = video.get("platform") == None
            if IS_DIRECT:
                if self.passed_params.get("download_file") == True:
                    TEMP_DIR = self.allocateTemp()
                    SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))

                    if video.get("files") != None:
                        VIDEO_URL = video.get("files").get("mp4_480")
                        # TODO hls download
                        if "srcIp=" not in VIDEO_URL:
                            logger.log(message=f"Video {VIDEO_ID} contains direct mp4; downloading",section="VkAttachments",name="message")
                            HTTP_REQUEST = await download_manager.addDownload(end=VIDEO_URL,dir=SAVE_PATH)
                            FILE = self._fileFromJson({
                                "extension": "mp4",
                                "upload_name": ORIGINAL_NAME,
                                "filesize": SAVE_PATH.stat().st_size,
                            })
                        else:
                            logger.log(message=f"Video {VIDEO_ID} has HLS; downloading",section="VkAttachments",name="message")
            else:
                logger.log(message=f"Video {VIDEO_ID} is from another platform ({video.get("platform")})",section="VkAttachments",name="message")
            
            ENTITY = self._entityFromJson({
                "suggested_name": VIDEO_NAME,
                "source": "vk:video"+str(VIDEO_ID),
                "internal_content": video,
                "file": FILE,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": video.get("date"),
            })
            __entities_list.append(ENTITY)

        return {
            "entities": __entities_list
        }
