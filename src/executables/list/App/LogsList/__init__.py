from executables.acts import Act
from resources.Consts import consts
from app.App import logger
from app.App import config

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return config.get("web.logs_watching.allow")

        return super().canBeUsedAt(at)

    async def execute(self, i = {}):
        logs_storage = logger.logs_storage
        dir_storage = logs_storage.dir

        log_files = dir_storage.glob('*.json')
        out_list = []
        
        for log_file in log_files:
            if log_file.is_file():
                out_list.append(log_file.name.replace(log_file.suffix, ""))

        return out_list
