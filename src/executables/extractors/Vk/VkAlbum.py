from resources.Globals import VkApi, logger, asyncio
from executables.extractors.Vk.VkBase import VkBase
from resources.Exceptions import NotFoundException

class VkAlbum(VkBase):
    name = 'VkAlbum'
    category = 'Vk'
    docs = {
        "description": {
            "name": {
                "ru": "VK Альбом",
                "en": "VK Album"
            },
            "definition": {
                "ru": "Метаинформация об альбоме VK",
                "en": "Metainfo about VK Album"
            }
        },
        "tags": ["deprecated"]
    }

    def declare():
        params = {}
        params["item_id"] = {
            "docs": {
                "definition": {
                    "ru": "ID альбома",
                    "en": "ID of album",
                }
            },
            "type": "string",
        }
        params["__json_info"] = {
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }

        return params

    async def recieveById(self, item_ids):
        ids = item_ids[0].split("_")
        return await self.__vkapi.call("photos.getAlbums", {"owner_id": ids[0], "album_ids": ids[1], "need_covers": 1, "photo_sizes": 1})

    async def run(self, args):
        self.__vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        albums = None
        __album_ids = self.passed_params.get("item_id")
        album_ids = __album_ids.split(",")
        if self.passed_params.get("__json_info") == None:
            try:
                __albums_resp = await self.recieveById(album_ids)
                if __albums_resp.get("items"):
                    albums = __albums_resp.get("items")
            except:
                albums = None
        else:
            try:
                albums = self.passed_params.get("__json_info")
                if type(__albums_resp) == dict:
                    albums = [__albums_resp]
            except:
                albums = None

        if albums == None or len(albums) < 1:
            raise NotFoundException("album not found")

        if self.passed_params.get("download_photos") == True:
            logger.log(message="This method is deprecated. Use Vk.VkSection instead!",section="VkCollection",name="deprecated")

        __entities_list = []
        __tasks = []
        for item in albums:
            __task = asyncio.create_task(self.__item(item, __entities_list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return {
            "entities": __entities_list
        }

    async def __item(self, item, link_entities):
        item["site"] = self.passed_params.get("vk_path")

        __ITEM_ID  = f"{item.get('owner_id')}_{item.get('id')}"
        __SOURCE   = f"vk:album{__ITEM_ID}"
        SUGGESTED_NAME = f"{item.get('title')} ({item.get('owner_id')}_{item.get('id')})"
        logger.log(message=f"Recieved album {__ITEM_ID}",section="VkCollection",name="message")

        ALBUM_ContentUnit = self._ContentUnitFromJson({
            "source": __SOURCE,
            "internal_content": item,
            "unlisted": 1,
            "suggested_name": SUGGESTED_NAME,
            "suggested_description": item.get("description"),
            "declared_created_at": item.get("date"),
        })
        link_entities.append(ALBUM_ContentUnit)
