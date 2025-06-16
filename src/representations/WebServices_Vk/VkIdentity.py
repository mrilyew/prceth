from representations.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from resources.Exceptions import NotFoundException
from resources.Consts import consts
from utils.MainUtils import entity_sign
from pathlib import Path
from app.App import logger
import os

class VkIdentity(BaseVkItemId):
    @classmethod
    def declare(cls):
        params = {}
        params["download_avatar"] = BooleanArgument({
            "default": True,
        })
        params["download_cover"] = BooleanArgument({
            "default": True,
        })

        return params

    class Extractor(BaseVkItemId.Extractor):
        async def __download_avatar(self, json):
            su = self.storageUnit()
            save_name = "avatar.jpg"
            save_path = Path(os.path.join(su.temp_dir, save_name))

            url = json.get("photo_max")
            if url == None:
                raise NotFoundException("ava not found")

            await download_manager.addDownload(dir=save_path,end=url)

            su.write_data({
                "extension": "jpg",
                "upload_name": save_name,
                "filesize": save_path.stat().st_size,
            })

            return su

        async def __download_cover(self, json):
            su = self.storageUnit()
            save_name = "cover.jpg"
            save_path = Path(os.path.join(su.temp_dir, save_name))

            cover = json.get("cover")
            if cover == None or cover.get('images') == None or len(cover.get("images")) < 1:
                raise NotFoundException("cover not found")

            images = cover.get("images")
            images_ = sorted(images, key=lambda x: (x['width'] is None, x['width']), reverse=True)
            image = images_[0]

            await download_manager.addDownload(dir=save_path,end=image.get("url"))

            su.write_data({
                "extension": "jpg",
                "upload_name": save_name,
                "filesize": save_path.stat().st_size,
            })

            return su

        async def __response(self, i = {}):
            ids = i.get('ids')
            identities_ids = ids.split(",")

            user_ids, group_ids, users, groups = [[], [], [], []]
            __users_response, __groups_response = [None, None]

            for _id in identities_ids:
                __id = int(_id)
                if __id > 0:
                    user_ids.append(__id)
                else:
                    group_ids.append(abs(__id))

            logger.log(message=f"Got ids +{','.join(str(x) for x in user_ids)}, -{','.join(str(x) for x in group_ids)}", section='VkEntities', kind='success')

            if len(user_ids) > 0:
                __users_response = await self.vkapi.call("users.get", {"user_ids": ",".join(str(x) for x in user_ids), "fields": ",".join(consts["vk.user_fields"])})
            if len(group_ids) > 0:
                __groups_response = await self.vkapi.call("groups.getById", {"group_ids": ",".join(str(x) for x in group_ids), "fields": ",".join(consts["vk.group_fields"])})

            if __users_response != None:
                for user in __users_response:
                    user["vkapi_type"] = "user"
                    users.append(user)

            if __groups_response != None:
                if 'groups' in __groups_response:
                    for club in __groups_response.get("groups"):
                        club["vkapi_type"] = "club"
                        groups.append(club)
                else:
                    for club in __groups_response:
                        club["vkapi_type"] = "club"
                        groups.append(club)

            return users + groups

        async def item(self, item, list_to_add):
            name = ""
            declared_date = None
            links = []

            if item.get("vkapi_type") == "user":
                name = f"VK User {item.get('first_name')} {item.get('last_name')}"
                declared_date = item.get("reg_date", None)
            else:
                name = f"VK Club {item.get('name')}"

            if self.args.get("download_avatar") == True:
                try:
                    ava = await self.__download_avatar(item)
                    item["relative_photo"] = entity_sign(ava)

                    links.append(ava)
                except Exception as _e:
                    logger.log(message='Avatar not found, not downloading', section='Vk!Identity', kind='error')

            if self.args.get("download_cover") == True:
                try:
                    cov = await self.__download_cover(item)
                    item["relative_cover"] = entity_sign(cov)

                    links.append(cov)
                except NotFoundException:
                    logger.log(message='Cover not found, not downloading', section='Vk!Identity', kind='error')
                except Exception as _e:
                    logger.logException(_e,section="Vk!Identity")

            logger.log(f"Got idents {item.get("vkapi_type")}{item.get('id')}",section="Vk!Identity",kind='success')

            cu = self.contentUnit({
                "source": {
                    'type': 'vk',
                    'vk_type': item.get("vkapi_type"),
                    'content': item.get('id')
                },
                "name": name,
                "content": item,
                "declared_created_at": declared_date,
                "links": links,
            })

            list_to_add.append(cu)
