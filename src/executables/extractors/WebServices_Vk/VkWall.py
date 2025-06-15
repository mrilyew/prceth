from declarable.ArgumentsTypes import IntArgument, StringArgument, CsvArgument, BooleanArgument, FloatArgument
from executables.extractors.Base.BaseTimeoutable import BaseTimeoutable
from representations.WebServices_Vk.VkPost import VkPost
from submodules.WebServices.VkApi import VkApi
from app.App import logger
import math, asyncio

class VkWall(BaseTimeoutable):
    category = 'WebServices_Vk'
    docs = {}

    @classmethod
    def declare(cls):
        params = {}
        params.update(VkPost.declareVk())
        params["owner_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["first_iteration"] = IntArgument({
            "default": 0
        })
        params["limit"] = IntArgument({
            "default": 0,
        })
        params["per_page"] = IntArgument({
            "default": 100
        })
        params["filter"] = StringArgument({
            "default": 'all',
        })
        params["attachments_info"] = CsvArgument({
            "default": "*",
        })
        params["attachments_file"] = CsvArgument({
            "default": "photo",
        })
        params["download_reposts"] = BooleanArgument({
            'default': True,
        })
        params["api_timeout"] = FloatArgument({
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        downloaded_count = 0
        owner_id = i.get('owner_id')
        filter_name = i.get('filter')
        limit_count = i.get('limit')
        first_iteration = i.get('first_iteration')
        per_page = i.get('per_page')
        vkapi = VkApi(token=i.get("api_token"),endpoint=i.get("api_url"))

        total_count = await VkPost.wallCount(vkapi, owner_id, filter_name)
        call_times = math.ceil(total_count / i.get('per_page'))

        logger.log(message=f"Total {total_count} items; will be {call_times} calls",section="Iterable!Vk",kind="message")

        for time in range(first_iteration, call_times):
            offset = per_page * time
            if limit_count > 0 and (downloaded_count > limit_count):
                break

            logger.log(message=f"{time + 1}/{call_times} time of items recieving; {offset} offset",section="Iterable!Vk",kind="message")

            response = await VkPost.wall(vkapi, owner_id=owner_id, filter=filter_name, count=per_page, offset=offset)
            items = await VkPost.extract({
                'object': response,
                'attachments_info': i.get('attachments_info'),
                'attachments_file': i.get('attachments_file'),
                'download_reposts': i.get('download_reposts'),
            })

            downloaded_count += len(items)

            if i.get("api_timeout") != 0:
                await asyncio.sleep(i.get("api_timeout"))

            for item in items:
                self.linked_dict.append(item)
