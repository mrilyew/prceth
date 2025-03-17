from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, config, utils, logger
from resources.Exceptions import NotFoundException

class VkAudio(VkTemplate):
    name = 'VkAudio'
    category = 'Vk'
    params = {
        "item_id": {
            "desc_key": "audio_id_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def passParams(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)
        self.passed_params["download_file"] = args.get("download_file", True)

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"

        super().passParams(args)
    
    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("audio.get", {"audio_ids": item_id, "extended": 1})
    
    async def run(self, args):
        __ITEM_RES = None
        AUDIO = None
        __SOURCE   = None
        __ITEM_ID  = self.passed_params.get("item_id")
        if self.passed_params.get("__json_info") == None:
            try:
                __ITEM_RES = await self.__recieveById(__ITEM_ID)
                AUDIO = __ITEM_RES.get("items")[0]
            except:
                AUDIO = None
        else:
            try:
                __ITEM_RES = self.passed_params.get("__json_info")
                AUDIO = __ITEM_RES
            except:
                AUDIO = None

        if AUDIO == None:
            raise NotFoundException("audio not found")
        
        if __ITEM_ID == None:
            __ITEM_ID  = f"{AUDIO.get("owner_id")}_{AUDIO.get("id")}"
            __SOURCE   = f"vk:audio{__ITEM_ID}"
        else:
            __SOURCE = f"vk:audio{__ITEM_ID}"

        logger.log(message=f"Recieved audio {__ITEM_ID}",section="VkAudio",name="message")

        ___OUT_FILE = None
        ___OUT_EXT  = "mp3"
        ___OUT_SIZE = 0

        AUDIO_NAME = f"{AUDIO.get("artist")} — {AUDIO.get("title")}"
        AUDIO_UPLOAD_NAME = utils.validName(AUDIO_NAME) + f".{___OUT_EXT}"
        ___SAVE_PATH = Path(os.path.join(self.temp_dir, AUDIO_UPLOAD_NAME))

        if self.passed_params.get("download_file") == False:
            logger.log(message=f"Do not downloading audio {__ITEM_ID} because download_file!=1",section="VkAudio",name="message")
        else:
            if AUDIO.get("url") == None:
                logger.log(message=f"Audio {__ITEM_ID} does not contains url to file",section="VkAudio",name="error")
            else:
                # Todo HLS
                if ".m3u8" in AUDIO.get("url"):
                    pass
                else:
                    DOWNLOAD_URL = AUDIO.get("url")
                    HTTP_REQUEST = await download_manager.addDownload(end=DOWNLOAD_URL,dir=___SAVE_PATH)

                    ___OUT_FILE = {
                        "extension": ___OUT_EXT,
                        "upload_name": AUDIO_UPLOAD_NAME,
                        "filesize": ___OUT_SIZE,
                    }

        AUDIO["site"] = self.passed_params.get("vk_path")
        __indexation = utils.clearJson(AUDIO)

        return {
            "entities": [
                {
                    "file": ___OUT_FILE,
                    "source": __SOURCE,
                    "indexation_content": __indexation,
                    "entity_internal_content": AUDIO
                }
            ]
        }
