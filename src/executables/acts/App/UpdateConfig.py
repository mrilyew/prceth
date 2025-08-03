from declarable.ArgumentsTypes import ObjectArgument
from executables.acts import BaseAct
from resources.Consts import consts
from app.App import app, config

class UpdateConfig(BaseAct):
    category = 'App'

    @classmethod
    def declare(cls):
        params = {}
        params["values"] = ObjectArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, args = {}):
        values = args.get("values")
        tabu = consts.get("config.hidden_values_spaces")

        assert values != None, "new values not passed"

        for i in enumerate(values):
            index = i[0]
            name = i[1]
            val = values.get(name)

            if val == None:
                continue

            config.set(name, val)

        return {
            "success": 1
        }
