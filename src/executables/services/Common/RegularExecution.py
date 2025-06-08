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

    def __get_executable(self, executable_name, executable_type):
        pass_args = parse_json(self.config.get("pass_args", "{}"))

        if self.c_cached_executable == None:
            match(executable_type):
                case "act":
                    self.c_cached_executable = ActsRepository().getByName(executable_name)
                case "extractor":
                    self.c_cached_executable = ExtractorsRepository().getByName(executable_name)

        if self.c_cached_executable == None:
            raise FatalError("executable not found")

    async def execute(self, i = {}):
        executable_type = self.config.get("executable_type")
        executable_name = self.config.get("executable_name")

        if executable_type == None:
            raise FatalError("executable_type is not passed in \"data\"")

        self.__get_executable(executable_name, executable_type)

        logger.log(message=f"Called {executable_name}", kind="message", section="Services")

        __exec = self.c_cached_executable()

        await __exec.safeExecute(args=pass_args)
