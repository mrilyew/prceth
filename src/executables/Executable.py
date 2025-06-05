from submodules.Files.FileManager import file_manager
from resources.Consts import consts
from app.App import config, storage, logger
from utils.MainUtils import get_ext, dump_json
from resources.Exceptions import ExecutableArgumentsException
from db.ContentUnit import ContentUnit
from declarable.DeclarableArgs import DeclarableArgs

class Executable:
    name = 'base'
    category = 'base'
    passed_params = {}
    params = {}
    after_save_actions = {}
    temp_dirs = []
    entities_buffer = []
    manual_params = False
    already_declared = False
    docs = {
        "description": {
            "name": {
                "en": "No name passed"
            },
            "definition": {
                "en": "No description passed"
            }
        }
    }
    events = {
        "success": [],
        "afterSave": [],
        "error": [],
    }
    main_args = {}

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
    
    async def safeExecute(self, args):
        res = None

        try:
            res = await self.execute(args=args)
        except Exception as x:
            logger.logException(x, section="Executables")
            self.onFail()

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

    # Comparisons

    @classmethod
    def isAbstract(cls):
        return cls.category.lower() in ["template", "base"]

    @classmethod
    def isHidden(cls):
        return getattr(cls, "hidden", False) == True

    @classmethod
    def canBeExecuted(cls):
        '''
        Is this Executable can be runned or it's technical
        '''
        return cls.isAbstract() == False and cls.isHidden() == False

    # Arguments

    def declare():
        '''
        Method that defines dictionary of current executable args
        '''
        params = {}

        return params

    def recursiveDeclare(self):
        ignore_list = self.main_args.get('ignore', [])

        if getattr(self, "already_declared", False) == True:
            return None

        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            final_params = {}
            new_params = __sub_class.declare()
            for i, name in enumerate(new_params):
                if name in ignore_list:
                    continue

                final_params[name] = new_params.get(name)

            self.params.update(final_params)

        self.already_declared = True

    def setArgs(self, args):
        self.params = {}
        #self.passed_params = {} # Resetting

        # Catching params from parent executables
        self.recursiveDeclare()

        MAX_OUTPUT_CHECK_PARAMS = self.params
        if MAX_OUTPUT_CHECK_PARAMS == None:
            return

        if getattr(self, "main_args") != None:
            MAIN_ARG_TYPE = self.main_args.get("type")

            if MAIN_ARG_TYPE == "and":
                for _arg in self.main_args.get("list"):
                    if _arg not in args:
                        raise ExecutableArgumentsException(f"Argument \"{_arg}\" not passed")
            elif MAIN_ARG_TYPE == "or" or MAIN_ARG_TYPE == "strict_or":
                passed_list_need = 0
                for _arg in self.main_args.get("list", []):
                    if _arg in args:
                        passed_list_need += 1

                if passed_list_need == 0:
                    raise ExecutableArgumentsException(f"Need at least 1 required argument")

                if MAIN_ARG_TYPE == "strict_or" and passed_list_need > 1:
                    raise ExecutableArgumentsException(f"Pass only 1 required argument (cuz \"strict_or\")")

        decl = DeclarableArgs(MAX_OUTPUT_CHECK_PARAMS, args)

        try:
            self.passed_params.update(decl.dict())
        except Exception as _j:
            if len(MAX_OUTPUT_CHECK_PARAMS) < 2:
                if consts.get("context") == "cli":
                    print("Usage:\n")

                    print(self.getUsageString(), end="")
                    exit()
                else:
                    raise _j
            else:
                raise _j

        if self.manual_params == True:
            self.passed_params.update(args)

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
