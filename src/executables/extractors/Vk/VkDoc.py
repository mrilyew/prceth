from executables.extractors.Vk.VkBase import VkBase
from resources.Globals import os, download_manager, VkApi, Path, asyncio, logger
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkDoc(VkBase):
    name = 'VkDoc'
    category = 'Vk'
    docs = {
        "description": {
            "name": {
                "ru": "VK Документ",
                "en": "VK Document"
            },
            "definition": {
                "ru": "Документ из vk",
                "en": "Document from vk"
            }
        },
    }
    file_containment = {
        "files_count": "1",
        "files_extensions": ["docx", "doc", "gif"]
    }

    def declare():
        params = {}
        params["item_id"] = {
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
            "type": "bool",
            "default": True
        }

        return params

    async def recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("docs.getById", {"docs": ",".join(item_ids), "extended": 1})

    async def run(self, args):
        DOCS_RESPONSE = []

        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")

        if self.passed_params.get("__json_info") == None:
            DOCS_RESPONSE = await self.recieveById(item_ids)
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
        __tasks = []
        for item in DOCS_RESPONSE:
            __task = asyncio.create_task(self.__item(item, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        item["site"] = self.passed_params.get("vk_path")

        __ITEM_ID, __SOURCE = [None, None]
        if __ITEM_ID == None:
            if item.get("owner_id") == None:
                __ITEM_ID = "url:" + item.get("private_url")
                __SOURCE  = __ITEM_ID
            else:
                __ITEM_ID  = f"{item.get('owner_id')}_{item.get('id')}"
                __SOURCE   = f"vk:doc{__ITEM_ID}"
        else:
            __SOURCE = f"vk:doc{__ITEM_ID}"

        logger.log(message=f"Recieved document {__ITEM_ID}",section="VkAttachments",name="message")

        item_EXT  = item.get("ext")
        item_TEXT = item.get("title") + "." + item_EXT
        item_URL  = item.get("url")
        item_SIZE = item.get("size", 0)

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
            "internal_content": item,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
        })

        link_entities.append(ENTITY)
