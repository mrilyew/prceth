from executables.representations.WebServices_Vk import BaseVkItemId
from declarable.ArgumentsTypes import ObjectArgument, StringArgument, BooleanArgument, CsvArgument
from repositories.RepresentationsRepository import RepresentationsRepository
from utils.MainUtils import proc_strtr
from app.App import logger

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
            return await self.vkapi.call("wall.getById", {"posts": (",".join(i.get('ids'))), "extended": 1})

        async def item(self, item, list_to_add):
            '''
            Converts VK Api Post object to readable format
            '''

            # deleting useless
            item.pop("track_code", None)
            item.pop("hash", None)

            # definings

            self.outer._insertVkLink(item, self.args.get('vk_path'))

            attachments = item.get('attachments', [])
            reposts = item.get('copy_history', [])
            item["relative_attachments"] = []
            item["relative_copy_history"] = []

            do_download_attachments = True
            do_download_reposts = self.args.get('download_reposts') == True

            # content unit parts

            item_id = f"{item.get('owner_id')}_{item.get('id')}"
            name = f"{self.outer.vk_type.title()} {str(item_id)}"
            if self.outer.vk_type == "message":
                item_id = f"{item.get('peer_id', item.get('from_id'))}_{item.get('id')}"

            if item.get('text') != None and type(item.get('text')) == str and len(item.get('text')) > 0:
                name = proc_strtr(item.get('text'), 100)

            logger.log(message=f"Recieved {self.outer.vk_type} {item_id}",section="Vk",kind=logger.KIND_MESSAGE)

            out = self.ContentUnit()

            for key, attachment in enumerate(attachments):
                try:
                    attachment_item = await self.format_attachment(key, attachment, out)
                    if attachment_item == False:
                        continue

                    item['relative_attachments'].append({
                        "type": attachment.get('type'),
                        f"{attachment.get('type')}": attachment_item.sign()
                    })
                except Exception as e:
                    logger.logException(e, "Vk", silent=False, prefix="Error processing attachment: ")

            if reposts != None and do_download_reposts:
                for key, repost in enumerate(reposts):
                    try:
                        repost_item = await self.format_repost(key, repost, out)

                        assert repost_item != None

                        item['relative_copy_history'].append(repost_item.sign())
                    except Exception as exc:
                        logger.logException(exc, "Vk", prefix="Error processing attachment: ")

            owner_keys = ['from_id', 'owner_id', 'copy_owner_id']
            for key in owner_keys:
                if item.get(key) != None and self.buffer.get('profiles') != None:
                    self.outer._insertOwner(item, key, self.buffer.get('profiles'), self.buffer.get('groups'))

            out.source = {
                'type': 'vk',
                'vk_type': self.outer.vk_type,
                'content': item_id
            }
            out.display_name = name
            out.content = item
            out.unlisted = self.args.get("unlisted") == 1
            out.declared_created_at = item.get("date")

            list_to_add.append(out)

        async def format_attachment(self, key, attachment, orig):
            '''
            Converts attachment dict to ContentUnit
            '''

            att_type = attachment.get("type")
            class_name = att_type
            if att_type == "wall":
                class_name = "post"

            att_object = attachment.get(att_type)
            if att_object == None:
                return None

            attachments_info = self.args.get('attachments_info')
            attachments_file = self.args.get('attachments_file')

            should_download_json = False
            should_download_file = False

            if len(attachments_info) > 0:
                should_download_json = attachments_info[0] == "*" or att_type in attachments_info

            if len(attachments_file) > 0:
                should_download_file = attachments_file[0] == "*" or att_type in attachments_file

            if should_download_json == False:
                return False

            attachment_name = f"WebServices_Vk.{class_name.title()}"
            attachment_representation = RepresentationsRepository().getByName(attachment_name)

            if attachment_representation == None:
                from representations.Data.Json import Json as UnknownAttachmentRepresentation

                logger.log(message="Recieved unknown attachment: " + str(class_name), section="Vk", kind=logger.KIND_MESSAGE)

                output = await UnknownAttachmentRepresentation().extract({
                    "object": attachment,
                })

                _item = output[0]
                _item.unlisted = True
                _item.save(force_insert=True)

                orig.add_link(_item)
            else:
                attachment_id = f"{att_object.get('owner_id')}_{att_object.get('id')}"
                att_class = attachment_representation()

                logger.log(message=f"Recieved attachment {str(class_name)} {attachment_id}",section="Vk",kind=logger.KIND_MESSAGE)

                output = await att_class.extract({
                    "object": att_object,
                    "api_url": self.args.get("api_url"),
                    "vk_path": self.args.get("vk_path"),
                    "download": should_download_file,
                })

                _item = output[0]
                _item.unlisted = True
                _item.save()

                orig.add_link(_item)

            return _item

        async def format_repost(self, key, repost, orig):
            repost_id = f"{repost.get('owner_id')}_{repost.get('id')}"
            if repost == None:
                return repost # epic

            logger.log(message=f"Found repost {key}",section="Vk",kind=logger.KIND_MESSAGE)

            repost_thing = Post()
            vals = await repost_thing.extract({
                "object": repost,
                "api_url": self.args.get("api_url"),
                "vk_path": self.args.get("vk_path"),
                "attachments_info": self.args.get("attachments_info"),
                "attachments_file": self.args.get("attachments_file"),
                "download_reposts": False,
            })

            _item = vals[0]
            _item.unlisted = True
            _item.save()

            orig.add_link(_item)
