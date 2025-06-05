from executables.services.Base.Base import BaseService
from utils.MainUtils import parse_json
from pathlib import Path
from app.App import logger
from resources.Consts import consts
from submodules.Files import FileManager
from repositories.ActsRepository import ActsRepository
from repositories.ExtractorsRepository import ExtractorsRepository
from app.App import config
import os, json, asyncio

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
        pass_args = parse_json(self.config.get("pass_args", "{}"))

        executable = None
        match(executable_type):
            case "act":
                executable = ActsRepository().getByName(executable_name)
            case "extractor":
                executable = ExtractorsRepository().getByName(executable_name)

        assert executable != None, "executable not found"

        __exec = self.fork(executable, pass_args)

        res = await __exec.execute(args=pass_args)

        return res
