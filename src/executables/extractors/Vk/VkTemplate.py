from executables.extractors.Base import BaseExtractor
from resources.Globals import config

class VkTemplate(BaseExtractor):
    name = 'VkTemplate'
    category = 'template'
    params = {
        "access_token": {
            "desc_key": "-",
            "type": "string",
            "default": config.get("vk.access_token", None),
            "assert": True,
        },
        "api_url": {
            "desc_key": "-",
            "type": "string",
            "default": config.get("vk.api_url", "api.vk.com/method"),
            "assert": True,
        },
        "vk_path": {
            "desc_key": "-",
            "type": "string",
            "default": config.get("vk.vk_path", "vk.com"),
            "assert": True,
        }
    }

    def setArgs(self, args, joined_args):
        print(self.params)
        super().setArgs(args, joined_args)

    async def run(self, args):
        pass
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get("vk_path")}/" + INPUT_ENTITY.orig_source
        }}
