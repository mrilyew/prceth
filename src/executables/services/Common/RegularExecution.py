from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json, often_params, ActsRepository, ExtractorsRepository
from executables.services.Base.Base import BaseService

class RegularExecution(BaseService):
    name = 'RegularExecution'
    category = 'Common'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        executable_type = self.config.get("executable_type")

        assert executable_type != None, "executable_type is not passed in \"data\""

        executable_name = self.config.get("executable_name")
        pass_args = utils.parse_json(self.config.get("pass_args", "{}"))

        executable = None
        match(executable_type):
            case "act":
                executable = ActsRepository().getByName(executable_name)
            case "extractor":
                executable = ExtractorsRepository().getByName(executable_name)

        assert executable != None, "executable not found"

        __exec = executable()
        __exec.setArgs(args=pass_args)

        res = await __exec.execute(args=pass_args)

        return res
