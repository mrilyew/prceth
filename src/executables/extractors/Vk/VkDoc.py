from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, json5, config, utils, logger
from resources.Exceptions import NotFoundException
from core.Wheels import metadata_wheel, additional_metadata_wheel
from db.File import File

# Downloads document from vk.com using api.
class VkDoc(VkTemplate):
    name = 'VkDoc'
    category = 'Vk'
    params = {
        "item_id": {
            "desc_key": "doc_id_desc",
            "type": "string",
            "maxlength": 3
        },
    }

    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"

        super().setArgs(args)
    
    async def __recieveById(self, item_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("docs.getById", {"docs": item_id, "extended": 1})
    
    async def run(self, args):
        __ITEM_RES = None
        __ITEM_ID  = self.passed_params.get("item_id")
        __SOURCE   = ""
        DOCUMENT = None
        if self.passed_params.get("__json_info") == None:
            __ITEM_RES = await self.__recieveById(__ITEM_ID)
            try:
                DOCUMENT = __ITEM_RES[0]
            except:
                DOCUMENT = None
        else:
            try:
                __ITEM_RES = self.passed_params.get("__json_info")
                DOCUMENT = __ITEM_RES
            except:
                DOCUMENT = None
        
        if DOCUMENT == None:
            raise NotFoundException("doc not found")
        
        if __ITEM_ID == None:
            if DOCUMENT.get("owner_id") == None:
                __ITEM_ID = "url:" + DOCUMENT.get("private_url")
                __SOURCE  = __ITEM_ID
            else:
                __ITEM_ID  = f"{DOCUMENT.get("owner_id")}_{DOCUMENT.get("id")}"
                __SOURCE   = f"vk:doc{__ITEM_ID}"
        else:
            __SOURCE = f"vk:doc{__ITEM_ID}"
        
        logger.log(message=f"Recieved document {__ITEM_ID}",section="VkDoc",name="message")

        item_EXT  = DOCUMENT.get("ext")
        item_TEXT = DOCUMENT.get("title") + "." + item_EXT
        item_URL  = DOCUMENT.get("url")
        item_SIZE = DOCUMENT.get("size", 0)
        save_path = Path(os.path.join(self.temp_dir, item_TEXT))

        HTTP_REQUEST = await download_manager.addDownload(end=item_URL,dir=save_path)
        DOCUMENT["site"] = self.passed_params.get("vk_path")
        __indexation = utils.clearJson(DOCUMENT)
        FILE = self._fileFromJson({
            "extension": item_EXT,
            "upload_name": item_TEXT,
            "filesize": item_SIZE,
        })
        ENTITY = self._entityFromJson({
            "file": FILE,
            "source": __SOURCE,
            "indexation_content": __indexation,
            "entity_internal_content": DOCUMENT,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        return {
            "entities": [
                ENTITY
            ]
        }
