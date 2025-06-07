from executables.services.Base.Base import BaseService
from utils.MainUtils import parse_json
from app.App import logger
from repositories.ActsRepository import ActsRepository
from repositories.ExtractorsRepository import ExtractorsRepository
from resources.Exceptions import FatalError

class RegularExecution(BaseService):
    category = 'Common'
    c_cached_executable = None
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, i = {}):
        executable_type = self.config.get("executable_type")

        if executable_type == None:
            raise FatalError("executable_type is not passed in \"data\"")

        executable_name = self.config.get("executable_name")
        pass_args = parse_json(self.config.get("pass_args", "{}"))

        if self.c_cached_executable == None:
            match(executable_type):
                case "act":
                    self.c_cached_executable = ActsRepository().getByName(executable_name)
                case "extractor":
                    self.c_cached_executable = ExtractorsRepository().getByName(executable_name)

        logger.log(message=f"Called {executable_name}", kind="message", section="Services")

        if self.c_cached_executable == None:
            raise FatalError("executable not found")

        __exec = self.c_cached_executable()

        return await __exec.safeExecute(args=pass_args)
