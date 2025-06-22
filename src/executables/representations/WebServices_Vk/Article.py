from executables.representations.WebServices_Vk import BaseVkItemId
from app.App import logger
from db.DbInsert import db_insert

class Article(BaseVkItemId):
    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids_string = i.get('ids')
            items_ids = items_ids_string.split(",")

            response = await self.vkapi.call("articles.getByLink", {"links": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))
            is_do_unlisted = self.args.get("unlisted") == 1

            title = item.get("title")
            date = item.get("published_date")

            logger.log(message=f"Recieved article {item.get('url')}",section="Vk!Article",kind=logger.KIND_MESSAGE)

            cu = db_insert.contentFromJson({
                "source": {
                    "type": 'url',
                    'content': item.get('url')
                },
                "content": item,
                "name": title,
                "unlisted": is_do_unlisted,
                "declared_created_at": date,
            })

            list_to_add.append(cu)
