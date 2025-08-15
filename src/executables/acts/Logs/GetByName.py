from declarable.ArgumentsTypes import StringArgument
from utils.MainUtils import parse_json
from executables.acts import BaseAct
from resources.Consts import consts
from app.App import logger, config

class GetByName(BaseAct):
    @classmethod
    def declare(cls):
        params = {}
        params["file"] = StringArgument({
            "default": None,
        })

        return params
    
    async def execute(self, args = {}):
        _file = args.get("file")

        if ".json" not in _file:
            _file = _file + ".json"

        if consts.get("context") == "web":
            assert config.get("web.logs_watching.allow") == True, "not allowed"

        logs_storage = logger.logs_storage
        dir_storage = logs_storage.dir

        log_file = dir_storage.joinpath(_file)

        assert log_file.is_file(), "not found"

        content = log_file.open().read()
        content_size = len(content)
        content_json = parse_json(content)

        return {
            "size": content_size,
            "logs": content_json,
        }
