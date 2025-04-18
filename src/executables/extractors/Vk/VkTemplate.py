from executables.extractors.Base import BaseExtractor
from resources.Globals import env

class VkTemplate(BaseExtractor):
    name = 'VkTemplate'
    category = 'template'

    def declare():
        params = {}
        params["access_token"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.access_token", None),
            "assert": {
                "assert_not_null": True,
            },
        }
        params["api_url"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.api_url", "api.vk.com/method"),
            "assert": {
                "assert_not_null": True,
            },
        }
        params["vk_path"] = {
            "desc_key": "-",
            "type": "string",
            "default": env.get("vk.vk_path", "vk.com"),
            "assert": {
                "assert_not_null": True,
            },
        }

        return params

    def setArgs(self, args):
        super().setArgs(args)

    async def run(self, args):
        pass
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get('vk_path')}/" + INPUT_ENTITY.orig_source
        }}
