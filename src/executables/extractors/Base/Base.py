from app.Logger import logger
from submodules.Files.FileManager import file_manager
from executables.Executable import Executable

class BaseExtractor(Executable):
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

        return params

    @classmethod
    def isCreatesCollection(cls):
        return getattr(cls, "_collection", None) != None
