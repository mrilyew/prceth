from executables.list.WebServices_Vk.Post import Post

class Message(Post):
    vk_type = "message"

    class Extractor(Post.Extractor):
        async def __response(self, i = {}):
            return await self.vkapi.call("messages.getById", {"message_ids": (",".join(i.get('ids'))), "extended": 1})
