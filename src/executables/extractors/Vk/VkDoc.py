from executables.extractors.Base import BaseExtractor
from resources.Globals import os, download_manager, ExecuteResponse, VkApi, Path, json5, config, utils
from resources.Exceptions import NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel

# Downloads document from vk.com using api.
class VkDoc(BaseExtractor):
    name = 'VkDoc'
    category = 'vk'
    params = {
        "item_id": {
            "desc_key": "doc_id_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def passParams(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["preset_json"] = args.get("preset_json", None)
        self.passed_params["access_token"] = args.get("access_token", config.get("vk.access_token", None))
        self.passed_params["api_url"] = args.get("api_url", "api.vk.com/method")
        self.passed_params["vk_path"] = args.get("vk_path", "vk.com")

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"
        assert self.passed_params.get("access_token") != None, "access_token not passed"
        assert self.passed_params.get("api_url") != None, "api_url not passed"
        assert self.passed_params.get("vk_path") != None, "vk_path not passed"
    
    async def __recieveById(self, photo_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("docs.getById", {"docs": photo_id, "extended": 1})
    
    async def run(self, args):
        __item_res = None
        __item_id  = self.passed_params.get("item_id")
        __source   = ""
        __item_obj = None
        if self.passed_params.get("preset_json") == None:
            __item_res = await self.__recieveById(__item_id)
            __item_obj = __item_res[0]
        else:
            __item_res = self.passed_params.get("preset_json")
            __item_obj = __item_res
        
        if __item_id == None:
            if __item_obj.get("owner_id") == None:
                __item_id = "url:" + __item_obj.get("private_url")
                __source  = __item_id
            else:
                __item_id  = f"{__item_obj.get("owner_id")}_{__item_obj.get("id")}"
                __source   = f"vk:doc{__item_id}"
        else:
            __source = f"vk:doc{__item_id}"
        
        item_EXT  = __item_obj.get("ext")
        item_TEXT = __item_obj.get("title") + "." + item_EXT
        item_URL  = __item_obj.get("url")
        save_path = Path(os.path.join(self.temp_dir, item_TEXT))

        HTTP_REQUEST = await download_manager.addDownload(end=item_URL,dir=save_path)

        return ExecuteResponse({
            "format": item_EXT,
            "original_name": str(item_TEXT),
            "filesize": __item_obj.get("size", 1),
            "source": __source,
            "entity_internal_content": __item_obj
        })

    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": "https://vk.com/" + INPUT_ENTITY.orig_source
        }}
