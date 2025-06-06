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

    async def safeExecute(self, args: dict)->dict:
        res = await self.execute(self.validate(args))

        return res

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

    # Factory

    def fork(self, extractor_name_or_class, args = None):
        '''
        Creates new executable by passed name or class.

        Params:

        extractor_name_or_class — full name or class of executable instance

        args — dict that will be passed to "setArgs"
        '''
        from repositories.ExtractorsRepository import ExtractorsRepository

        _ext = None
        if type(extractor_name_or_class) == str:
            _ext = (ExtractorsRepository()).getByName(extractor_name_or_class)
        else:
            _ext = extractor_name_or_class

        if _ext == None:
            return None

        ext = _ext()
        if args != None:
            ext.setArgs(args)

        return ext

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

    async def _execute_sub(self, extractor, extractor_params, array_link):
        try:
            extractor.setArgs(extractor_params)
            executed = await extractor.execute({})
            for ___item in executed.get("entities"):
                array_link.append(___item)
        except Exception as ___e:
            logger.logException(input_exception=___e,section="Extractor",silent=False)
