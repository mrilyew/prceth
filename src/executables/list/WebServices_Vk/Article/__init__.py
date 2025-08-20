from executables.list.WebServices_Vk import BaseVkItemId
from app.App import logger

class Implementation(BaseVkItemId):
    class Extractor(BaseVkItemId.Extractor):
        async def __response(self, i = {}):
            items_ids = i.get('ids')

            response = await self.vkapi.call("articles.getByLink", {"links": (",".join(items_ids)), "extended": 1})

            return response

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.args.get('vk_path'))

            out = self.ContentUnit()
            out.display_name = item.get("title")
            out.content = item
            out.unlisted = self.args.get("unlisted") == 1
            out.declared_created_at = item.get("published_date")
            out.source = {
                "type": 'url',
                'content': item.get('url')
            }

            logger.log(message=f"Recieved article {item.get('url')}",section="Vk",kind=logger.KIND_MESSAGE)

            list_to_add.append(out)
