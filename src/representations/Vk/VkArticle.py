from representations.Vk.BaseVk import BaseVk, VkExtractStrategy
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from app.App import logger

class VkArticle(BaseVk):
    category = 'Vk'

    def declare():
        params = {}
        params["item_id"] = StringArgument({})
        params["object"] = ObjectArgument({})

        return params

    class Extractor(VkExtractStrategy):
        def extractWheel(self, i = {}):
            if i.get('object') != None:
                return 'extractByObject'
            elif 'item_id' in i:
                return 'extractById'

        async def extractById(self, i = {}):
            items_ids_string = i.get('item_id')
            items_ids = items_ids_string.split(",")

            response = await self.vkapi.call("articles.getByLink", {"links": (",".join(items_ids)), "extended": 1})

            return await self.gatherList(response, self.item)

        async def extractByObject(self, i = {}):
            final_object = i.get("object")
            if type(final_object) != list:
                final_object = [final_object]

            return await self.gatherList(final_object, self.item)

        async def item(self, item, list_to_add):
            self.outer._insertVkLink(item, self.buffer.get('args').get('vk_path'))
            is_do_unlisted = self.buffer.get('args').get("unlisted") == 1

            title = item.get("title")
            date = item.get("published_date")

            logger.log(message=f"Recieved article {item.get('url')}",section="VkEntity",kind="message")

            cu = self.contentUnit({
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
