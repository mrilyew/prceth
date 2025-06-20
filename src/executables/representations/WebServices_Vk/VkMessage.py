from representations.WebServices_Vk.VkPost import VkPost

class VkMessage(VkPost):
    vk_type = "message"

    class Extractor(VkPost.Extractor):
        async def __response(self, i = {}):
            items_ids_str = i.get('ids')
            items_ids = items_ids_str.split(",")

            response = await self.vkapi.call("messages.getById", {"message_ids": (",".join(items_ids)), "extended": 1})

            return response
