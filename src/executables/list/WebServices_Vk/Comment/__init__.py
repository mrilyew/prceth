from executables.list.WebServices_Vk import Post

class Implementation(Post):
    vk_type = "comment"

    class Extractor(Post.Extractor):
        async def __response(self, i = {}):
            ids = i.get('ids')
            output = {
                'items': [],
                'profiles': [],
                'groups': [],
            }

            for in_id in ids:
                id_list = in_id.split('_')
                response = await self.vkapi.call("wall.getComment", {"owner_id": id_list[0], "comment_id": id_list[1], "extended": 1})

                if type(response) == dict and 'items' in response:
                    for __item in response.get('items'):
                        output['items'].append(__item)

                    for __item in response.get('profiles'):
                        output['profiles'].append(__item)

                    for __item in response.get('groups'):
                        output['groups'].append(__item)

            return output
