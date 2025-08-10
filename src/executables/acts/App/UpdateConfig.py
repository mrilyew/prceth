from declarable.ArgumentsTypes import ObjectArgument, LimitedArgument
from executables.acts import BaseAct
from resources.Consts import consts
from app.App import config, env

class UpdateConfig(BaseAct):
    @classmethod
    def declare(cls):
        params = {}
        params["type"] = LimitedArgument({
            "default": "config",
            "values": ["config", "env"]
        })
        params["values"] = ObjectArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, args = {}):
        values = args.get("values")
        act_type = args.get("type")
        tabu = consts.get("config.hidden_values_spaces")

        assert values != None, "new values not passed"

        if act_type == "config":
            assert config.get("web.config_editing.allow") == True, "editing is not allowed"
        elif act_type == "env":
            assert config.get("web.env_editing.allow") == True, "env editing is not allowed"

        for i in enumerate(values):
            index = i[0]
            name = i[1]
            val = values.get(name)
            no = False

            if act_type == "config":
                for _name in tabu:
                    if name.startswith(_name):
                        no = True

            if no == True or val == None:
                continue

            if act_type == "config":
                config.set(name, val)
            elif act_type == "env":
                env.set(name, val) 

        return {
            "success": 1
        }
