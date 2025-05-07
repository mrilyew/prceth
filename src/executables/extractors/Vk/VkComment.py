from executables.extractors.Vk.VkPost import VkPost
from resources.Globals import VkApi

class VkComment(VkPost):
    name = 'VkComment'
    category = 'Vk'
    vk_type = "comment"
    docs = {
        "description": {
            "name": {
                "ru": "VK Комментарий",
                "en": "VK Comment"
            },
            "definition": {
                "ru": "Информация о комментарии VK",
                "en": "Metainfo about VK comment"
            }
        }
    }

    async def recieveById(self, post_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        comment_id = post_ids[0].split("_")
        return await __vkapi.call("wall.getComment", {"owner_id":comment_id[0], "comment_id": comment_id[1], "extended": 1})
