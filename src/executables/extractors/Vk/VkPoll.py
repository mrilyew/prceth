from resources.Globals import VkApi, asyncio, logger, Path, download_manager, os
from executables.extractors.Vk.VkBase import VkBase
from resources.Exceptions import NotFoundException

# Downloads document from vk.com using api.
class VkPoll(VkBase):
    name = 'VkPoll'
    category = 'Vk'
    hidden = True

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "vk_poll_desc",
            "type": "string",
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
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
    
    async def recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        spl = item_ids[0].split("_")

        return await __vkapi.call("polls.getById", {"owner_id": spl[0], "poll_id": spl[1], "extended": 1})
    
    async def run(self, args):
        __item_ids = self.passed_params.get("item_id")
        item_ids = __item_ids.split(",")
        items = None

        if self.passed_params.get("__json_info") == None:
            try:
                item_resp = await self.recieveById(item_ids)
                if item_resp != None:
                    items = [item_resp]
            except:
                items = None
        else:
            try:
                items = self.passed_params.get("__json_info")
                if type(items) == dict:
                    items = [items]
            except:
                items = None

        if items == None or len(items) < 1:
            raise NotFoundException("poll not found")
        
        __entities_list = []
        __tasks = []
        for poll in items:
            __task = asyncio.create_task(self.__item(poll, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        item["site"] = self.passed_params.get("vk_path")

        # TODO: background downloader
        __ITEM_ID  = f"{item.get('owner_id')}_{item.get('id')}"
        __SOURCE   = f"vk:poll{__ITEM_ID}"

        logger.log(message=f"Recieved poll {__ITEM_ID}",section="VkAttachments",name="message")
        __FILE = None

        if self.passed_params.get("download_file") == True:
            ORIGINAL_NAME = f"poll{__ITEM_ID}.jpg"
            try:
                TEMP_DIR = self.allocateTemp()

                if item.get("photo") != None:
                    __photo_sizes = sorted(item.get("photo").get("images"), key=lambda x: (x['width'] is None, x['width']), reverse=True)
                    __optimal_size = __photo_sizes[0]

                    SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))
                    HTTP_REQUEST = await download_manager.addDownload(end=__optimal_size.get("url"),dir=SAVE_PATH)
                    FILE_SIZE = SAVE_PATH.stat().st_size
                    __FILE = self._fileFromJson({
                        "extension": "jpg",
                        "upload_name": ORIGINAL_NAME,
                        "filesize": FILE_SIZE,
                    }, TEMP_DIR)

                    item["relative_photo"] = f"__lcms|file_{__FILE.id}"

                    logger.log(message=f"Downloaded poll {__ITEM_ID} background",section="VK",name="success")
            except FileNotFoundError as _ea:
                pass
                logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VK",name="error")

        ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "internal_content": item,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
            "suggested_name": item.get("question"),
            "linked_files": [__FILE],
        })
        link_entities.append(ENTITY)
