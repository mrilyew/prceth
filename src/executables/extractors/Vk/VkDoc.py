from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, json5, config, utils, logger
from resources.Exceptions import NotFoundException
from db.File import File

# Downloads document from vk.com using api.
class VkDoc(VkTemplate):
    name = 'VkDoc'
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
        return await __vkapi.call("docs.getById", {"docs": ",".join(item_ids), "extended": 1})
    
    async def run(self, args):
        DOCS_RESPONSE = []

        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")

        if self.passed_params.get("__json_info") == None:
            DOCS_RESPONSE = await self.__recieveById(item_ids)
        else:
            try:
                DOCS_RESPONSE = self.passed_params.get("__json_info")
                if type(DOCS_RESPONSE) == dict:
                    DOCS_RESPONSE = [DOCS_RESPONSE]
            except:
                DOCS_RESPONSE = None
        
        if DOCS_RESPONSE == None or len(DOCS_RESPONSE) < 1:
            raise NotFoundException("doc not found")
        
        __entities_list = []
        for DOC in DOCS_RESPONSE:
            DOC["site"] = self.passed_params.get("vk_path")

            __ITEM_ID, __SOURCE = [None, None]
            if __ITEM_ID == None:
                if DOC.get("owner_id") == None:
                    __ITEM_ID = "url:" + DOC.get("private_url")
                    __SOURCE  = __ITEM_ID
                else:
                    __ITEM_ID  = f"{DOC.get('owner_id')}_{DOC.get('id')}"
                    __SOURCE   = f"vk:doc{__ITEM_ID}"
            else:
                __SOURCE = f"vk:doc{__ITEM_ID}"

            logger.log(message=f"Recieved document {__ITEM_ID}",section="VkAttachments",name="message")

            item_EXT  = DOC.get("ext")
            item_TEXT = DOC.get("title") + "." + item_EXT
            item_URL  = DOC.get("url")
            item_SIZE = DOC.get("size", 0)
            
            FILE = None
            if self.passed_params.get("download_file") == True:
                TEMP_DIR = self.allocateTemp()

                save_path = Path(os.path.join(TEMP_DIR, item_TEXT))
                HTTP_REQUEST = await download_manager.addDownload(end=item_URL,dir=save_path)
                FILE = self._fileFromJson({
                    "extension": item_EXT,
                    "upload_name": item_TEXT,
                    "filesize": item_SIZE,
                })

            ENTITY = self._entityFromJson({
                "file": FILE,
                "suggested_name": item_TEXT,
                "source": __SOURCE,
                "internal_content": DOC,
                "unlisted": self.passed_params.get("unlisted") == 1,
                "declared_created_at": DOC.get("date"),
            })

            __entities_list.append(ENTITY)

        return {
            "entities": __entities_list
        }
