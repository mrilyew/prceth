from resources.Globals import file_manager, logger
from executables.Executable import Executable

class BaseExtractor(Executable):
    name = 'base'

    def __init__(self, del_dir_on_fail=True, need_preview=True, write_mode=None):
        self.passed_params = {}
        #if temp_dir != None:
            #self.temp_dir_prefix = temp_dir
        self.temp_dir_prefix = None

        self.temp_dirs = []
        self.del_dir_on_fail = del_dir_on_fail
        self.need_preview = need_preview
        if write_mode != None:
            self.write_mode = write_mode

        self.defineConsts()

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

    @classmethod
    def isCreatesCollection(cls):
        return getattr(cls, "_collection", None) != None
