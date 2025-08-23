from executables.acts import Act
from declarable.Arguments import BooleanArgument, ActArgument
from resources.Consts import consts

# internal usage only!

class Implementation(Act):
    executable_cfg = {
        'free_args': True
    }
    available = []

    @classmethod
    def declare(cls):
        params = {}
        params["i"] = ActArgument({
            "assertion": {
                "not_null": True
            }
        })
        params["ignore_requirements"] = BooleanArgument({
            'default': False,
        })

        return params

    async def execute(self, i = {}):
        act_class = i.get("i")
        ignore_requirements = i.get("ignore_requirements")

        if consts.get("context") != "cli":
            assert act_class.canBeUsedAt(consts.get("context"))

        if ignore_requirements == False:
            assert act_class.isModulesInstalled()

        act = act_class()
        act_response = await act.safeExecute(i)

        return act_response
