from submodules.Files.FileManager import file_manager
from resources.Consts import consts
from app.App import config, storage, logger
from utils.MainUtils import get_ext, dump_json
from db.ContentUnit import ContentUnit
from declarable.ArgsValidator import ArgsValidator
from executables.Runnable import Runnable

class Executable(Runnable):
    after_save_actions = {}
    temp_dirs = []
    entities_buffer = []
    manual_params = False
    already_declared = False
    events = {
        "success": [],
        "afterSave": [],
        "error": [],
    }
    declaration_cfg = {}

    def __init__(self):
        def __onerror(exception):
            logger.logException(exception, section="Executables")

        def __onsuccess():
            try:
                ___ln = len(self.entities_buffer)
                __msg = f"Saving total {str(___ln)} entities;"
                if ___ln > 100:
                    __msg += " do not turn off your computer."

                logger.log(__msg,section="ContentUnitSaveMechanism",name="success")
            except Exception as _x:
                print("PostRun:" + str(_x))
                pass

            for unsaved_ContentUnit in self.entities_buffer:
                self._ContentUnitPostRun(unsaved_ContentUnit)

        self.events.get("error").append(__onerror)
        #self.events.get("success").append(__onsuccess)

    # Execution

    async def execute(self, args):
        pass

    async def safeExecute(self, args: dict)->dict:
        res = None

        try:
            __validated_args = ArgsValidator().validate(self.recursiveDeclaration(), args, self.declaration_cfg)

            res = await self.execute(args=__validated_args)
        except Exception as x:
            logger.logException(x, section="Executables")
            self.onError(x)

            raise x

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

    def getUsageString(self):
        _p = ""
        for id, param in enumerate(getattr(self, "params", {})):
            __lang = config.get("ui.lang")
            __param = getattr(self, "params", {}).get(param)
            __docs = __param.get("docs")
            if __docs != None:
                __definition = __docs.get("definition")
                __values = __docs.get("values")

                _p += (f"{param}: {__definition.get(__lang, __definition.get("en"))}\n")

        return _p

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
            pass
