from resources.Globals import config, VkApi, logger, utils, math, asyncio
from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from resources.Exceptions import NotFoundException

class VkAlbum(VkTemplate):
    name = 'VkAlbum'
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
        params["download_photos"] = {
            "desc_key": "-",
            "type": "bool",
            "default": False
        }
        params["download_file"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }
        params["rev"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True
        }
        params["download_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0, # for paranoic people
        }
        params["api_timeout"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["limit"] = {
            "desc_key": "-",
            "type": "int",
            "default": 0,
        }
        params["per_page"] = {
            "desc_key": "-",
            "type": "int",
            "default": 100
        }

        return params
    
    async def __recieveById(self, item_ids):
        ids = item_ids[0].split("_")
        return await self.__vkapi.call("photos.getAlbums", {"owner_id": ids[0], "album_ids": ids[1], "need_covers": 1, "photo_sizes": 1})

    async def run(self, args):
        self.__vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        albums = None
        __album_ids = self.passed_params.get("item_id")
        album_ids = __album_ids.split(",")
        if self.passed_params.get("__json_info") == None:
            try:
                __albums_resp = await self.__recieveById(album_ids)
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
            logger.log(message="Bro! This method is deprecated! Use Vk.VkSection instead!",section="VkCollection",name="deprecated")

        __entities_list = []
        for album in albums:
            album["site"] = self.passed_params.get("vk_path")

            __ITEM_ID  = f"{album.get("owner_id")}_{album.get("id")}"
            __SOURCE   = f"vk:album{__ITEM_ID}"
            SUGGESTED_NAME = f"{album.get("title")} ({album.get("owner_id")}_{album.get("id")})"
            logger.log(message=f"Recieved album {__ITEM_ID}",section="VkCollection",name="message")

            ALBUM_ENTITY = self._entityFromJson({
                "source": __SOURCE,
                "internal_content": album,
                "unlisted": 1,
                "suggested_name": SUGGESTED_NAME,
                "suggested_description": album.get("description"),
                "declared_created_at": album.get("date"),
            })

            photos_list = []
            if self.passed_params.get("download_photos") == True:
                __per_page = self.passed_params.get("per_page")
                __count = album.get("size")
                __downloaded_count = 0
                times = math.ceil(__count / __per_page)
                vphoto_ext = VkPhoto(need_preview=self.need_preview)

                for time in range(0, times):
                    OFFSET = __per_page * time

                    logger.log(message=f"{time + 1}/{times} time of photos recieving; {OFFSET} offset",section="VkCollection",name="message")

                    _ID = __ITEM_ID.split("_")
                    photos_api = await self.__vkapi.call("photos.get", {"owner_id": _ID[0], 
                                                                        "album_id": _ID[1], 
                                                                        "rev": int(self.passed_params.get("rev")), 
                                                                        "extended": 1,
                                                                        "photo_sizes": 1,
                                                                        "offset": OFFSET,
                                                                        "count": __per_page})
                    
                    for photo_item in photos_api.get("items"):
                        if self.passed_params.get("limit") > 0 and (__downloaded_count > self.passed_params.get("limit")):
                            break
                        
                        __PHOTO_ID = str(photo_item.get("owner_id")) + "_" + str(photo_item.get("id"))
                        vphoto_ext.setArgs({
                            "unlisted": 0,
                            "item_id": __PHOTO_ID,
                            "__json_info": photo_item,
                            "access_token": self.passed_params.get("access_token"),
                            "api_url": self.passed_params.get("api_url"),
                            "vk_path": self.passed_params.get("vk_path"),
                            "download_file": self.passed_params.get("download_file"),
                        })

                        try:
                            executed = await vphoto_ext.execute({})
                            for __photo in executed.get("entities"):
                                photos_list.append(__photo)
                                
                        except Exception:
                            pass
                        
                        if self.passed_params.get("download_timeout") != 0:
                            await asyncio.sleep(self.passed_params.get("download_timeout"))

                        __downloaded_count += 1
                    
                    if self.passed_params.get("api_timeout") != 0:
                        await asyncio.sleep(self.passed_params.get("api_timeout"))
            
                await vphoto_ext.postRun(return_entities=photos_list)
                del vphoto_ext
            
            if len(photos_list) > 0:
                __entities_list.append(ALBUM_ENTITY)
                fnl = {
                    "entities": __entities_list,
                    "collection": {
                        "suggested_name": SUGGESTED_NAME,
                        "suggested_description": album.get("description"),
                        "declared_created_at": album.get("date"),
                    },
                }
                return fnl
            else:
                return {
                    "entities": [ALBUM_ENTITY]
                }
