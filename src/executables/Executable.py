from submodules.Files.FileManager import file_manager
from resources.Consts import consts
from app.App import config, storage, logger
from utils.MainUtils import get_ext, dump_json
from db.ContentUnit import ContentUnit
from executables.Runnable import Runnable

class Executable(Runnable):
    events = {
        "success": [],
        "afterSave": [],
        "error": [],
    }

    def __init__(self):
        def __onerror(exception):
            logger.logException(exception, section="Executables")

        self.events.get("error").append(__onerror)
        #self.events.get("success").append(__onsuccess)

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict):
        return await self.execute(self.validate(args))

    # Events

    async def onError(self, exception: Exception):
        for __closure in self.events.get("error"):
            await __closure(exception)

    async def onAfterSave(self, entities):
        for __closure in self.events.get("afterSave"):
            await __closure(entities)

    async def onSuccess(self):
        for __closure in self.events.get("success"):
            await __closure()

    # Documentation

    def manual(self):
        manual = {}
        __docs = getattr(self, "docs")
        __params = getattr(self, "params")
        __meta = __docs.get("description")

        manual["description"] = __meta
        manual["files"] = getattr(self, "file_containment", {})
        manual["params"] = __params

        return manual

    def describe(self):
        rt = {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
        }
        rt["meta"] = self.manual()

        return rt

    def self_insert(self, json_data: dict):
        json_data['extractor'] = self.full_name()

        return json_data
