from resources.Globals import config, VkApi, logger, utils, math, asyncio
from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from resources.Exceptions import NotFoundException

class VkAlbum(VkTemplate):
    name = 'VkAlbum'
    category = 'Vk'

    def setArgs(self, args):
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["__json_info"] = args.get("__json_info", None)
        self.passed_params["download_photos"] = int(args.get("download_photos", "1")) == 1
        self.passed_params["rev"] = int(args.get("rev", "0")) == 1
        self.passed_params["download_timeout"] = int(args.get("timeout", "0")) # for paranoic people
        self.passed_params["api_timeout"] = int(args.get("timeout", "0"))
        self.passed_params["limit"] = int(args.get("limit", "0"))

        assert self.passed_params.get("item_id") != None or self.passed_params.get("preset_json") != None, "item_id not passed"

        super().setArgs(args)
    
    async def __recieveById(self, item_id):
        return await self.__vkapi.call("photos.getAlbums", {"owner_id": 0, "album_ids": item_id, "need_covers": 1, "photo_sizes": 1})

    async def run(self, args):
        self.__vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        __ITEM_RES = None
        ALBUM = None
        __SOURCE   = None
        __ITEM_ID  = self.passed_params.get("item_id")
        if self.passed_params.get("__json_info") == None:
            try:
                __ITEM_RES = await self.__recieveById(__ITEM_ID)
                ALBUM = __ITEM_RES.get("items")[0]
            except:
                ALBUM = None
        else:
            try:
                __ITEM_RES = self.passed_params.get("__json_info")
                ALBUM = __ITEM_RES
            except:
                ALBUM = None

        if ALBUM == None:
            raise NotFoundException("album not found")
        
        if __ITEM_ID == None:
            __ITEM_ID  = f"{ALBUM.get("owner_id")}_{ALBUM.get("id")}"
            __SOURCE   = f"vk:album{__ITEM_ID}"
        else:
            __SOURCE = f"vk:album{__ITEM_ID}"

        logger.log(message=f"Recieved album {__ITEM_ID}",section="VkCollection",name="message")

        ALBUM["site"] = self.passed_params.get("vk_path")
        __indexation = utils.clearJson(ALBUM)
        ALBUM_ENTITY = self._entityFromJson({
            "source": __SOURCE,
            "indexation_content": __indexation,
            "internal_content": ALBUM,
            "unlisted": self.passed_params.get("unlisted") == 1,
        })

        if self.passed_params.get("download_photos") == True:
            __per_page = 100
            __count = ALBUM.get("size")
            __downloaded_count = 0
            times   = math.ceil(__count / __per_page)

            final_entites_list = []
            final_entites_list.append(ALBUM_ENTITY)

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
                    vphoto_ext = VkPhoto(need_preview=self.need_preview)
                    vphoto_ext.setArgs({
                        "unlisted": 0,
                        "item_id": __PHOTO_ID,
                        "__json_info": photo_item,
                        "access_token": self.passed_params.get("access_token"),
                        "api_url": self.passed_params.get("api_url"),
                        "vk_path": self.passed_params.get("vk_path"),
                        "download_file": 1,
                    })

                    try:
                        executed = await vphoto_ext.execute({})
                        for __photo in executed.get("entities"):
                            final_entites_list.append(__photo)
                    except Exception:
                        pass
                    
                    del vphoto_ext

                    if self.passed_params.get("download_timeout") != 0:
                        await asyncio.sleep(self.passed_params.get("download_timeout"))

                    __downloaded_count += 1
                
                if self.passed_params.get("api_timeout") != 0:
                    await asyncio.sleep(self.passed_params.get("api_timeout"))
            
            return {
                "entities": final_entites_list,
                "collection": {
                    "suggested_name": f"Vk Album {__ITEM_ID}",
                },
            }
        
        return {
            "entities": [
                ALBUM_ENTITY
            ]
        }
