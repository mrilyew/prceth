from resources.Globals import config
from executables.extractors.Base import BaseExtractor

class VkAlbum(BaseExtractor):
    name = 'VkAlbum'
    category = 'Vk'
    
    def passParams(self, args):
        self.passed_params = args
        self.passed_params["item_id"] = args.get("item_id")
        self.passed_params["preset_json"] = args.get("preset_json", None)
        self.passed_params["access_token"] = args.get("access_token", config.get("vk.access_token", None))
        self.passed_params["api_url"] = args.get("api_url", "api.vk.com/method")
        self.passed_params["vk_path"] = args.get("vk_path", "vk.com")
        self.passed_params["rev"] = args.get("rev", 0)
        self.passed_params["download_photos"] = args.get("download_photos", 0)

        super().passParams(args)

    async def run(self, args):
        # Recieving album info
        pass
