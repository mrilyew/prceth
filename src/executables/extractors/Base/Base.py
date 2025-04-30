from resources.Globals import file_manager, logger
from executables.Executable import Executable

class BaseExtractor(Executable):
    name = 'base'

    def __init__(self, temp_dir=None, del_dir_on_fail=True, need_preview=True, write_mode=2):
        self.passed_params = {}
        #if temp_dir != None:
            #self.temp_dir_prefix = temp_dir
        self.temp_dir_prefix = None

        self.temp_dirs = []
        self.del_dir_on_fail = del_dir_on_fail
        self.need_preview = need_preview
        self.write_mode = int(write_mode)
        self.defineConsts()

    @classmethod
    def isRunnable(cls):
        return cls.category.lower() not in ["template", "base"] and getattr(cls, "hidden", False) == False

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

    async def run(self, args):
        pass

    async def postRun(self, return_entities):
        if self.write_mode == 1:
            try:
                ___ln = len(self.unsaved_entities)
                __msg = f"Saving total {str(___ln)} entities;"
                if ___ln > 100:
                    __msg += " do not turn off your computer."
                
                logger.log(__msg,section="EntitySaveMechanism",name="success")
            except Exception as _x:
                print(_x)
                pass

            for unsaved_entity in self.unsaved_entities:
                unsaved_entity.save()

                try:
                    logger.log(f"Saved entity {str(unsaved_entity.id)} 👍",section="EntitySaveMechanism",name="success")
                except Exception as _x:
                    print(_x)
                    pass

    def describeSource(self, INPUT_ENTITY):
        return {"type": "none", "data": {
            "source": None
        }}

    async def execute(self, args):
        EXTRACTOR_RESULTS = None

        try:
            EXTRACTOR_RESULTS = await self.run(args=args)
        except Exception as x:
            logger.logException(x, section="Exctractors")
            self.onFail()

            raise x

        return EXTRACTOR_RESULTS
