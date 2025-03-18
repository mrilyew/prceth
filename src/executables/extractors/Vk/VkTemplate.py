from executables.extractors.Base import BaseExtractor
from resources.Globals import config

class VkTemplate(BaseExtractor):
    name = 'VkTemplate'
    category = 'template'
    
    def setArgs(self, args):
        self.passed_params["access_token"] = args.get("access_token", config.get("vk.access_token", None))
        self.passed_params["api_url"] = args.get("api_url", config.get("vk.api_url", "api.vk.com/method"))
        self.passed_params["vk_path"] = args.get("vk_path", config.get("vk.vk_path", "vk.com"))

        assert self.passed_params.get("access_token") != None, "access_token not passed"
        assert self.passed_params.get("api_url") != None, "api_url not passed"
        assert self.passed_params.get("vk_path") != None, "vk_path not passed"

        super().setArgs(args)

    async def run(self, args):
        pass
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get("vk_path")}/" + INPUT_ENTITY.orig_source
        }}
