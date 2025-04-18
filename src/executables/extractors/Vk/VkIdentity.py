from resources.Globals import os, VkApi, logger, consts, Path, download_manager
from executables.extractors.Vk.VkTemplate import VkTemplate
from executables.extractors.Vk.VkPhoto import VkPhoto
from resources.Exceptions import NotFoundException

class VkIdentity(VkTemplate):
    name = 'VkIdentity'
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["download_avatar"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }
        params["download_cover"] = {
            "desc_key": "-",
            "type": "bool",
            "default": True,
        }
        params["__json_info"] = {
            "desc_key": "-",
            "type": "object",
            "hidden": True,
            "assertion": {
                "assert_link": "item_id"
            }
        }

        return params

    async def run(self, args):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        identities_id_string = self.passed_params.get("item_id", "")
        IDENTITIES_IDS = identities_id_string.split(",")
        users   = []
        groups  = []
        __users_response, __groups_response = [[], []]

        if self.passed_params.get("__json_info") == None:
            user_ids = []
            group_ids = []

            for IDENTITY_ID in IDENTITIES_IDS:
                __id = int(IDENTITY_ID)
                if __id > 0:
                    user_ids.append(__id)
                else:
                    group_ids.append(abs(__id))

            logger.log(message=f"Got ids +{",".join(str(x) for x in user_ids)}, -{",".join(str(x) for x in group_ids)}")

            if len(user_ids) > 0:
                __users_response = await __vkapi.call("users.get", {"user_ids": ",".join(str(x) for x in user_ids), "fields": ",".join(consts["vk.user_fields"])})
            if len(group_ids) > 0:
                __groups_response = await __vkapi.call("groups.getById", {"group_ids": ",".join(str(x) for x in group_ids), "fields": ",".join(consts["vk.group_fields"])})
        else:
            json_inf = self.passed_params.get("__json_info")
        
            if type(json_inf) == dict:
                if json_inf.get("first_name") != None:
                    __users_response.append(json_inf)
                else:
                    __groups_response.append(json_inf)
            elif type(json_inf) == list:
                for __item in json_inf:
                    if __item.get("first_name") != None:
                        __users_response.append(__item)
                    else:
                        __groups_response.append(__item)
        
        async def __download_avatar(json):
            TEMP_DIR = self.allocateTemp()
            ORIGINAL_NAME = "avatar.jpg"
            SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))
            
            URL = json.get("photo_max")
            if URL == None:
                raise NotFoundException("ava not found")
            
            await download_manager.addDownload(dir=SAVE_PATH,end=URL)
            
            __file = self._fileFromJson({
                "extension": "jpg",
                "upload_name": ORIGINAL_NAME,
                "filesize": SAVE_PATH.stat().st_size,
            }, TEMP_DIR)

            return __file
                
        async def __download_cover(json):
            TEMP_DIR = self.allocateTemp()
            ORIGINAL_NAME = "cover.jpg"
            SAVE_PATH = Path(os.path.join(TEMP_DIR, ORIGINAL_NAME))

            cover = json.get("cover")
            if cover == None or len(cover.get("images")) < 1:
                raise NotFoundException("cover not found")
            
            images = cover.get("images")
            images_ = sorted(images, key=lambda x: (x['width'] is None, x['width']))
            image = images_[0]
            
            await download_manager.addDownload(dir=SAVE_PATH,end=image.get("url"))

            __file = self._fileFromJson({
                "extension": "jpg",
                "upload_name": ORIGINAL_NAME,
                "filesize": SAVE_PATH.stat().st_size,
            }, TEMP_DIR)

            return __file
        
        if __users_response != None:
            for user in __users_response:
                user["vkapi_type"] = "user"
                users.append(user)
        
        if type(__groups_response) != "dict":
            for club in __groups_response:
                club["vkapi_type"] = "club"
                groups.append(club)
        else:
            for club in __groups_response.get("groups"):
                club["vkapi_type"] = "club"
                groups.append(club)
        
        entities = []
        for identity in groups + users:
            name = ""
            source = ""
            reg_date = None
            linked_files = []

            if identity.get("vkapi_type") == "user":
                name = f"@vk_user: {identity.get("first_name")} {identity.get("last_name")}"
                source = f"vk:id{identity.get("id")}"
                reg_date = identity.get("reg_date", None)
            else:
                name = f"@vk_club: {identity.get("name")}"
                source = f"vk:group{identity.get("id")}"
            
            if self.passed_params.get("download_avatar") == True:
                try:
                    __file = await __download_avatar(identity)
                    __file.moveTempDir()
                    identity["relative_photo_max_orig"] = f"__lcms|file_{__file.id}"

                    linked_files.append(__file)
                except Exception as _e:
                    logger.logException(_e,section="Vk",noConsole=False)
                            
            if self.passed_params.get("download_cover") == True:
                try:
                    __file = await __download_cover(identity)
                    __file.moveTempDir()
                    identity["relative_cover"] = f"__lcms|file_{__file.id}"
                    
                    linked_files.append(__file)
                except NotFoundException:
                    pass
                except Exception as _e:
                    logger.logException(_e,section="Vk",noConsole=False)
            
            ENTITY = self._entityFromJson({
                "source": source,
                "suggested_name": name,
                "internal_content": identity,
                "declared_created_at": reg_date,
                "linked_files": linked_files,
            })
            entities.append(ENTITY)
        
        return {
            "entities": entities
        }
