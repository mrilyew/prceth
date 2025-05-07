from executables.extractors.Vk.VkPost import VkPost
from resources.Globals import VkApi

class VkMessage(VkPost):
    name = 'VkMessage'
    category = 'Vk'
    vk_type = "message"
    docs = {
        "description": {
            "name": {
                "ru": "VK Сообщение",
                "en": "VK Message"
            },
            "definition": {
                "ru": "Информация о сообщении VK",
                "en": "Metainfo about VK message"
            }
        }
    }

    async def recieveById(self, message_ids):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))

        return await __vkapi.call("messages.getById", {"message_ids": ",".join(message_ids), "extended": 1})
