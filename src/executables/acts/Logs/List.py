from executables.acts import BaseAct
from resources.Consts import consts
from app.App import logger
from app.App import config

class List(BaseAct):
    @classmethod
    def declare(cls):
        params = {}

        return params
    
    async def execute(self, args = {}):
        if consts.get("context") == "web":
            assert config.get("web.logs_watching.allow") == True, "not allowed"

        logs_storage = logger.logs_storage
        dir_storage = logs_storage.dir

        log_files = dir_storage.glob('*.json')
        out_list = []
        
        for log_file in log_files:
            if log_file.is_file():
                out_list.append(log_file.name.replace(log_file.suffix, ""))

        return out_list
