from executables.services.Base.Base import BaseService
from app.App import logger
from repositories.ActsRepository import ActsRepository
from repositories.ExtractorsRepository import ExtractorsRepository
from resources.Exceptions import FatalError
from declarable.ArgumentsTypes import LimitedArgument, StringArgument, ObjectArgument

class RegularExecution(BaseService):
    category = 'Common'
    c_cached_executable = None
    pass_args = {}

    @classmethod
    def declare(cls):
        params = {}
        params["executable_type"] = LimitedArgument({
            "values": ["act", "extractor"],
            "assertion": {
                "not_null": True,
            },
        })
        params["executable_name"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["pass_args"] = ObjectArgument({
            "default": {},
            "assertion": {
                "not_null": True,
            },
        })

        return params

    def __get_executable(self, executable_name, executable_type):
        self.pass_args = self.config.get("pass_args", {})

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

        logger.log(message=f"Called {executable_name}", kind="message", section=logger.SECTION_SERVICES)

        __exec = self.c_cached_executable()

        res = await __exec.safeExecute(args=self.pass_args)
        if executable_type == "act":
            print(res)
