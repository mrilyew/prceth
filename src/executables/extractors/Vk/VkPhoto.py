from executables.extractors.Vk.VkTemplate import VkTemplate
from resources.Globals import os, download_manager, VkApi, Path, json5, config, utils, logger, asyncio
from resources.Exceptions import NotFoundException

# Downloads photo from vk.com using api.
class VkPhoto(VkTemplate):
    name = 'VkPhoto'
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
    
    async def recieveById(self, item_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("photos.getById", {"photos": ",".join(item_ids), "extended": 1, "photo_sizes": 1})
    
    async def run(self, args):
        # TODO add check for real links like vk.com/photo1_1
        final_photos_objects = None
        i_photo_ids = self.passed_params.get("item_id")
        photo_ids = i_photo_ids.split(",")
        
        if self.passed_params.get("__json_info") == None:
            assert len(photo_ids) > 0, "item_id's not passed"
            final_photos_objects = await self.recieveById(photo_ids)
        else:
            final_photos_objects = self.passed_params.get("__json_info")
            if type(final_photos_objects) == dict:
                final_photos_objects = [final_photos_objects]
        
        __entities_list = []
        __tasks = []
        for photo in final_photos_objects:
            __task = asyncio.create_task(self.__item(photo, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        item["site"] = self.passed_params.get("vk_path")

        PHOTO_ID = f"{item.get('owner_id')}_{item.get('id')}"
        ORIGINAL_NAME = f"photo_{PHOTO_ID}_{item.get('date')}.jpg"
        
        logger.log(message=f"Recieved photo {PHOTO_ID}",section="VK",name="message")
    
        # So, downloading photo
        PHOTO_URL = ""
        if item.get("orig_photo") != None:
            PHOTO_URL = item.get("orig_photo").get("url")
        else:
            if item.get("url") != None:
                PHOTO_URL = item.get("url")
            else:
                try:
                    __photo_sizes = sorted(item.get("sizes"), key=lambda x: (x['width'] is None, x['width']), reverse=True)
                    __optimal_size = __photo_sizes[0]
                    # For old photos without sizes.
                    if __optimal_size.get("height") == 0:
                        __optimal_size = item.get("sizes")[-1]
                    
                    PHOTO_URL = __optimal_size.get("url")
                except Exception as ___e:
                    logger.logException(___e, section="Vk")
        
        if self.passed_params.get("download_file") == True:
            __FILE = None
            try:
                TEMP_DIR = self.allocateTemp()

                SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))
                HTTP_REQUEST = await download_manager.addDownload(end=PHOTO_URL,dir=SAVE_PATH)
                FILE_SIZE = SAVE_PATH.stat().st_size
                __FILE = self._fileFromJson({
                    "extension": "jpg",
                    "upload_name": ORIGINAL_NAME,
                    "filesize": FILE_SIZE,
                }, TEMP_DIR)

                logger.log(message=f"Downloaded photo {PHOTO_ID}",section="VK",name="success")
            except FileNotFoundError as _ea:
                logger.log(message=f"Photo's file cannot be found. Probaly broken file? Exception: {str(_ea)}",section="VK",name="error")
            
        ENTITY = self._entityFromJson({
            "file": __FILE,
            "suggested_name": f"VK Photo {str(PHOTO_ID)}",
            "source": "vk:photo"+str(PHOTO_ID),
            "internal_content": item,
            "unlisted": self.passed_params.get("unlisted") == 1,
            "declared_created_at": item.get("date"),
        }, TEMP_DIR)
        link_entities.append(ENTITY)
