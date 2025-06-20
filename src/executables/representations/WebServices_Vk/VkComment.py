from representations.WebServices_Vk.VkPost import VkPost

class VkComment(VkPost):
    vk_type = "comment"

    class Extractor(VkPost.Extractor):
        async def __response(self, i = {}):
            items_ids_str = i.get('ids')
            items_ids = items_ids_str.split(",")
            final_response = {
                'items': [],
                'profiles': [],
                'groups': [],
            }

            assert len(items_ids) < 5, 'bro too many'

            for id in items_ids:
                spl = id.split('_')
                response = await self.vkapi.call("wall.getComment", {"owner_id": spl[0], "comment_id": spl[1], "extended": 1})

                if type(response) == dict and 'items' in response:
                    for __item in response.get('items'):
                        final_response['items'].append(__item)

                    for __item in response.get('profiles'):
                        final_response['profiles'].append(__item)

                    for __item in response.get('groups'):
                        final_response['groups'].append(__item)

            return final_response
