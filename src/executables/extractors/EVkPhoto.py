from executables.extractors.Base import BaseExtractor
from resources.Globals import os, download_manager, ExecuteResponse, VkApi, Path, json5
from resources.Exceptions import NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel

# Downloads photo from vk.com using api.
class EVkPhoto(BaseExtractor):
    name = 'EVkPhoto'
    category = 'vk'
    params = {
        "photo_id": {
            "desc_key": "photo_id_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def dump(self, info):
        self.__predumped_info = info

    def passParams(self, args):
        self.passed_params["photo_id"] = args.get("photo_id")
        self.passed_params["access_token"] = args.get("access_token")
        self.passed_params["api_url"] = args.get("api_url", "api.vk.com/method")

        assert self.passed_params.get("photo_id") != None, "photo_id not passed"
        assert self.passed_params.get("access_token") != None, "access_token not passed"
        assert self.passed_params.get("api_url") != None, "api_url not passed"
    
    async def __recieveById(self, photo_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("photos.getById", {"photos": photo_id, "extended": 1})
    
    async def run(self, args):
        # TODO add check for real links like vk.com/photo1_1
        __photo_res = None
        __photo_id  = self.passed_params.get("photo_id")
        if getattr(self, "__predumped_info", None) == None:
            __photo_res = await self.__recieveById(__photo_id)
        else:
            __photo_res = self.__predumped_info
        
        __photo_obj = __photo_res[0]
        original_name = "photo.jpg"
        save_path = Path(os.path.join(self.temp_dir, original_name))
        
        PHOTO_URL = ""
        if __photo_obj.get("orig_photo") != None:
            PHOTO_URL = __photo_obj.get("orig_photo").get("url")
        else:
            __photo_sizes = sorted(__photo_obj.get("sizes"), key=lambda size: size.width)
            PHOTO_URL = __photo_sizes.get("url")
        
        HTTP_REQUEST = await download_manager.addDownload(end=PHOTO_URL,dir=save_path)

        return ExecuteResponse(
            format="jpg",
            original_name=original_name,
            filesize=save_path.stat().st_size,
            source="vk:"+__photo_id,
            json_info=__photo_obj
        )
