from app.Logger import logger
from submodules.Files.FileManager import file_manager
from executables.Executable import Executable

class BaseExtractor(Executable):
    def defineConsts(self):
        pass

    def declare():
        params = {}
        params["display_name"] = {
            "name": "display_name",
            "type": "string",
            "default": None,
        }
        params["description"] = {
            "name": "description",
            "type": "string",
            "default": None,
        }
        params["unlisted"] = {
            "name": "unlisted",
            "type": "bool",
            "default": False,
        }
        params["make_preview"] = {
            "name": "make_preview",
            "type": "bool",
            "default": True,
        }

        return params

    def onFail(self):
        if self.del_dir_on_fail == True:
            for t_dir in self.temp_dirs:
                try:
                    file_manager.rmdir(t_dir)
                except Exception:
                    logger.logException(t_dir, "Extractor", silent=False)

    @classmethod
    def isCreatesCollection(cls):
        return getattr(cls, "_collection", None) != None
