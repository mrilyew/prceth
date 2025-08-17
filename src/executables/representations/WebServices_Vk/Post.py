from executables.representations.WebServices_Vk import BaseVkItemId
from declarable.ArgumentsTypes import ObjectArgument, StringArgument, BooleanArgument, CsvArgument
from repositories.RepresentationsRepository import RepresentationsRepository
from utils.MainUtils import proc_strtr
from app.App import logger
from db.DbInsert import db_insert

class Post(BaseVkItemId):
    vk_type = 'post'

    @classmethod
    def declare(cls):
        params = {}
        params["object"] = ObjectArgument({})
        params["ids"] = StringArgument({})
        params["attachments_info"] = CsvArgument({
            'default': '*'
        })
        params["attachments_file"] = CsvArgument({
            'default': 'photo'
        })
        params["download_reposts"] = BooleanArgument({
            'default': True,
        })
        return params

    async def wallCount(vkapi, owner_id, filter):
        resp = await vkapi.call('wall.get', {
            'owner_id': owner_id,
            'filter': filter,
            'count': 1,
        })

        return resp.get('count')

    async def wall(vkapi, owner_id, filter, count=100, offset=0):
        response = await vkapi.call('wall.get', {
            'owner_id': owner_id,
            'filter': filter,
            'offset': offset,
            'count': count,
        })

        return response

    class Extractor(BaseVkItemId.Extractor):
        def preExecute(self, i):
            super().preExecute(i)
            self.buffer['attachments_info'] = i.get("attachments_info")
            self.buffer['attachments_file'] = i.get("attachments_file")

        async def __response(self, i = {}):
            items_ids = i.get('ids')

            response = await self.vkapi.call("wall.getById", {"posts": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, list_to_add):
            '''
            Converts VK Api Post object to readable format
            '''

            attachments_list = item.get('attachments', [])
            reposts_list = item.get('copy_history', [])

            is_do_unlisted = self.args.get("unlisted") == 1
            do_download_attachments = True
            do_download_reposts = self.args.get('download_reposts') == True

            item["relative_attachments"] = []
            item["relative_copy_history"] = []

            self.outer._insertVkLink(item, self.args.get('vk_path'))

            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            if self.outer.vk_type == "message":
                item_id = f"{item.get('peer_id', item.get('from_id'))}_{item.get('id')}"

            item.pop("track_code", None)
            item.pop("hash", None)

            logger.log(message=f"Recieved {self.outer.vk_type} {item_id}",section="Vk!Post",kind="message")

            links = []

            for key, attachment in enumerate(attachments_list):
                try:
                    attachment_item = await self.format_attachment(key, attachment, links)

                    if attachment_item != None:
                        item['relative_attachments'].append({
                            "type": attachment.get('type'),
                            f"{attachment.get('type')}": attachment_item.sign()
                        })
                except ModuleNotFoundError:
                    pass
                except Exception as exc:
                    logger.logException(exc, "Vk!Post", silent=False)

            if reposts_list != None and do_download_reposts:
                for key, repost in enumerate(reposts_list):
                    try:
                        repost_item = await self.format_repost(key, repost, links)

                        if repost_item != None:
                            item['relative_copy_history'].append(repost_item.sign())
                    except ModuleNotFoundError:
                        pass
                    except Exception as exc:
                        logger.logException(exc, "Vk!Post", silent=False)

            _name = f"{self.outer.vk_type.title()} {str(item_id)}"
            if item.get('text') != None and type(item.get('text')) == str and len(item.get('text')) > 0:
                _name = proc_strtr(item.get('text'), 100)

            owner_keys = ['from_id', 'owner_id', 'copy_owner_id']
            for key in owner_keys:
                if item.get(key) != None and self.buffer.get('profiles') != None:
                    self.outer._insertOwner(item, key, self.buffer.get('profiles'), self.buffer.get('groups'))

            _item_cu = db_insert.contentFromJson({
                "source": {
                    'type': 'vk',
                    'vk_type': self.outer.vk_type,
                    'content': item_id
                },
                "name": _name, # TODO:
                "content": item,
                "links": links,
                "unlisted": is_do_unlisted,
                "declared_created_at": item.get("date"),
            })

            list_to_add.append(_item_cu)

        async def format_attachment(self, key, attachment, linked_dict):
            '''
            Converts attachment dict to ContentUnit
            '''

            att_type = attachment.get("type")
            att_class_name = att_type
            att_object = attachment.get(att_type)

            if att_object == None:
                return None

            if att_type == "wall":
                att_class_name = "post"

            attachments_info = self.args.get('attachments_info')
            attachments_file = self.args.get('attachments_file')

            should_download_json = False
            should_download_file = False

            if len(attachments_info) > 0:
                should_download_json = attachments_info[0] == "*" or att_type in attachments_info

            if len(attachments_file) > 0:
                should_download_file = attachments_file[0] == "*" or att_type in attachments_file

            if should_download_json == False:
                return None

            attachment_object = None
            attachment_name = f"WebServices_Vk.{att_class_name.title()}"
            attachment_representation = RepresentationsRepository().getByName(attachment_name)
            if attachment_representation == None:
                from representations.Data.Json import Json as UnknownAttachmentRepresentation

                logger.log(message="Recieved unknown attachment: " + str(att_class_name), section="Vk!Post", kind=logger.KIND_MESSAGE)

                resl = await UnknownAttachmentRepresentation().extract({
                    "unlisted": True,
                    "object": attachment,
                })

                attachment_object = resl[0]
                attachment_object.save(force_insert=True)

                linked_dict.append(attachment_object)
            else:
                attachment_id = f"{att_object.get('owner_id')}_{att_object.get('id')}"
                att_class = attachment_representation()

                logger.log(message=f"Recieved attachment {str(att_class_name)} {attachment_id}",section="Vk!Post",kind=logger.KIND_MESSAGE)

                resl = await att_class.extract({
                    "unlisted": True,
                    "object": att_object,
                    "api_url": self.args.get("api_url"),
                    "vk_path": self.args.get("vk_path"),
                    "download": should_download_file,
                })

                attachment_object = resl[0]
                attachment_object.save(force_insert=True)

                linked_dict.append(attachment_object)

            return attachment_object

        async def format_repost(self, key, repost, linked_dict):
            repost_id = f"{repost.get('owner_id')}_{repost.get('id')}"
            if repost == None:
                return None

            logger.log(message=f"Found repost {key}",section="Vk!Post",kind=logger.KIND_MESSAGE)

            repost_thing = Post()
            vals = await repost_thing.extract({
                "unlisted": True,
                "object": repost,
                "api_url": self.args.get("api_url"),
                "vk_path": self.args.get("vk_path"),
                "attachments_info": self.args.get("attachments_info"),
                "attachments_file": self.args.get("attachments_file"),
                "download_reposts": False,
            })

            vk_post = vals[0]
            linked_dict.append(vk_post)

            return vk_post
