from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, config, utils, logger
from resources.Exceptions import NotFoundException

class VkAudio(VkTemplate):
    name = 'VkAudio'
    category = 'Vk'
    
    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }

        return params
    
    async def __recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("audio.get", {"audio_ids": ",".join(item_ids), "extended": 1})
    
    async def run(self, args):
        __audio_response = None
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        if self.passed_params.get("__json_info") == None:
            try:
                __audio_response = await self.__recieveById(item_ids)
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
        for audio in __audio_response:
            audio["site"] = self.passed_params.get("vk_path")

            __ITEM_ID = f"{audio.get('owner_id')}_{audio.get('id')}"
            __SOURCE  = f"vk:audio{__ITEM_ID}"

            logger.log(message=f"Recieved audio {__ITEM_ID}",section="VkAttachments",name="message")

            FILE = None
            ___OUT_EXT  = "mp3"
            ___OUT_SIZE = 0

            AUDIO_NAME = f"{audio.get('artist')} — {audio.get('title')}"
            AUDIO_UPLOAD_NAME = utils.validName(AUDIO_NAME) + f".{___OUT_EXT}"

            if self.passed_params.get("download_file") == True:
                TEMP_DIR = self.allocateTemp()
                ___SAVE_PATH = Path(os.path.join(TEMP_DIR, AUDIO_UPLOAD_NAME))

                if audio.get("url") == None:
                    logger.log(message=f"Audio {__ITEM_ID} does not contains url to file",section="VkAudio",name="error")
                else:
                    # Todo HLS
                    if ".m3u8" in audio.get("url"):
                        logger.log(message=f"Found .m3u8 of audio {__ITEM_ID}",section="VkAudio",name="message")
                        pass
                    else:
                        logger.log(message=f"Downloading raw .mp3 of audio {__ITEM_ID}",section="VkAudio",name="message")

                        DOWNLOAD_URL = audio.get("url")
                        HTTP_REQUEST = await download_manager.addDownload(end=DOWNLOAD_URL,dir=___SAVE_PATH)
                        ___OUT_SIZE = ___SAVE_PATH.stat().st_size

                        FILE = self._fileFromJson({
                            "extension": ___OUT_EXT,
                            "upload_name": AUDIO_UPLOAD_NAME,
                            "filesize": ___OUT_SIZE,
                        })
            
            ENTITY = self._entityFromJson({
                "source": __SOURCE,
                "internal_content": audio,
                "suggested_name": AUDIO_NAME,
                "file": FILE,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": audio.get("date"),
            })
            __entities_list.append(ENTITY)
        
        return {
            "entities": __entities_list
        }
