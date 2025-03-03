from executables.extractors.Base import BaseExtractor
from resources.Globals import VkApi, ExecuteResponse, json, utils, config

class EVkPost(BaseExtractor):
    name = 'EVkPost'
    category = 'vk'

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def passParams(self, args):
        self.passed_params = args
        self.passed_params["post_id"] = args.get("post_id")
        self.passed_params["access_token"] = args.get("access_token", config.get("vk.access_token", None))
        self.passed_params["api_url"] = args.get("api_url", "api.vk.com/method")
        self.passed_params["vk_path"] = args.get("vk_path", "vk.com")

        assert self.passed_params.get("post_id") != None, "post_id not passed"
        assert self.passed_params.get("access_token") != None, "access_token not passed"
        assert self.passed_params.get("api_url") != None, "api_url not passed"
        assert self.passed_params.get("vk_path") != None, "vk_path not passed"

        super().passParams(args)

    async def __recieveById(self, photo_id):
        __vkapi = VkApi(token=self.passed_params.get("access_token"),endpoint=self.passed_params.get("api_url"))
        return await __vkapi.call("wall.getById", {"posts": photo_id, "extended": 1})

    async def run(self, args):
        # TODO add check for real links like vk.com/wall1_1
        __post_res = None
        __post_id  = self.passed_params.get("post_id")
        if getattr(self, "__predumped_info", None) == None:
            __post_res = await self.__recieveById(__post_id)
        else:
            __post_res = self.__predumped_info
        
        # TODO: Attachments processing
        __post_obj = __post_res.get("items")[0]
        del __post_obj["track_code"]
        del __post_obj["hash"]

        __json_info = utils.clearJson(__post_obj)
        __json_info["site"] = self.passed_params.get("vk_path")

        return ExecuteResponse(
            original_name="Post №"+__post_id,
            filesize=len(json.dumps(__post_obj)),
            source="vk:wall"+__post_id,
            json_info=__json_info,
            summary=__post_obj,
            no_file=True,
        )

    def describeSource(self, INPUT_ENTITY):
        return {"type": "vk", "data": {
            "source": f"https://{INPUT_ENTITY.getFormattedInfo().get("vk_path")}/" + INPUT_ENTITY.orig_source
        }}
