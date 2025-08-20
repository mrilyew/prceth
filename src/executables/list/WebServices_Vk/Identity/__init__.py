from executables.list.WebServices_Vk import BaseVkItemId
from submodules.Web.DownloadManager import download_manager
from declarable.ArgumentsTypes import BooleanArgument
from utils.MainUtils import proc_strtr
from resources.Consts import consts
from pathlib import Path
from app.App import logger
import os

class Implementation(BaseVkItemId):
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
            url = json.get("photo_id")

            assert url != None

            main_su = self.StorageUnit()
            save_path = Path(os.path.join(main_su.temp_dir, "avatar.jpg"))

            await download_manager.addDownload(dir=save_path,end=url)

            main_su.set_main_file(save_path)

            return main_su

        async def __download_cover(self, json):
            cover = json.get("cover")

            assert cover != None and cover.get("images") != None and len(cover.get("images")) > 0

            main_su = self.StorageUnit()
            save_path = Path(os.path.join(main_su.temp_dir, "cover.jpg"))

            images = cover.get("images")
            images_ = sorted(images, key=lambda x: (x['width'] is not None, x['width']), reverse=True)
            image = images_[0]

            assert image != None

            await download_manager.addDownload(dir=save_path,end=image.get("url"))

            main_su.set_main_file(save_path)

            return main_su

        async def __response(self, i = {}):
            user_ids, group_ids = [[], []]
            output = []

            for _id in i.get('ids'):
                _id = int(_id)
                if _id > 0:
                    user_ids.append(_id)
                else:
                    group_ids.append(abs(_id))

            logger.log(message=f"Got ids +{','.join(str(x) for x in user_ids)}, -{','.join(str(x) for x in group_ids)}", section='Vk', kind=logger.KIND_SUCCESS)

            if len(user_ids) > 0:
                users = await self.vkapi.call("users.get", {"user_ids": ",".join(str(x) for x in user_ids), "fields": ",".join(consts["vk.user_fields"])})

                for user in users:
                    output.append(user)

            if len(group_ids) > 0:
                groups = await self.vkapi.call("groups.getById", {"group_ids": ",".join(str(x) for x in group_ids), "fields": ",".join(consts["vk.group_fields"])})

                if 'groups' in groups:
                    for club in groups.get("groups"):
                        output.append(club)
                else:
                    for club in groups:
                        output.append(club)

            return output

        async def item(self, item, list_to_add):
            name = ""
            declared_date = None

            if 'first_name' in item:
                item['vkapi_type'] = 'user'
            else:
                item['vkapi_type'] = 'group'

            if item.get("vkapi_type") == "user":
                name = f"{item.get('first_name')} {item.get('last_name')}"
                declared_date = item.get("reg_date", None)
            else:
                name = f"{item.get('name')}"

            out = self.ContentUnit()
            out.display_name = proc_strtr(name, 200)
            out.content = item
            out.source = {
                'type': 'vk',
                'vk_type': item.get("vkapi_type"),
                'content': item.get('id')
            }
            out.declared_created_at = declared_date

            if self.args.get("download_avatar") == True:
                try:
                    ava = await self.__download_avatar(item)
                    item["relative_photo"] = ava.sign()

                    out.add_link(ava)
                except Exception as _e:
                    logger.logException(_e,section="Vk",prefix="Could not download avatar: ")

            if self.args.get("download_cover") == True:
                try:
                    cov = await self.__download_cover(item)
                    item["relative_cover"] = cov.sign()

                    out.add_link(cov)
                except Exception as _e:
                    logger.logException(_e,section="Vk",prefix="Could not download cover: ")

            logger.log(f"Got id {item.get("vkapi_type")}{item.get('id')}",section="Vk",kind=logger.KIND_SUCCESS)

            list_to_add.append(out)
