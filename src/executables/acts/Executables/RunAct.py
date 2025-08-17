from executables.acts import BaseAct
from declarable.ArgumentsTypes import StringArgument, BooleanArgument
from repositories.ActsRepository import ActsRepository
from resources.Consts import consts

# internal usage only!

class RunAct(BaseAct):
    executable_cfg = {
        'free_args': True
    }
    available = []

    @classmethod
    def declare(cls):
        params = {}
        params["i"] = StringArgument({
            "assertion": {
                "not_null": True
            }
        })
        params["ignore_requirements"] = BooleanArgument({
            'default': False,
        })

        return params

    async def execute(self, i = {}):
        act_name = i.get("i")
        ignore_requirements = i.get("ignore_requirements")
        act_class = ActsRepository().getByName(plugin_name=act_name)

        assert act_class != None, "act not found"

        if consts.get("context") != "cli":
            assert act_class.canBeUsedAt(consts.get("context"))

        if ignore_requirements == False:
            assert act_class.isModulesInstalled()

        act = act_class()
        act_response = await act.safeExecute(i)

        return act_response
