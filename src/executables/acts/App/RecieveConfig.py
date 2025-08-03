from executables.acts import BaseAct
from resources.Consts import consts
from app.App import config

class RecieveConfig(BaseAct):
    category = 'App'

    async def execute(self, args = {}):
        result = []
        tabu = consts.get("config.hidden_values_spaces")

        assert config.get("web.config_editing.allow") == True, "editing is not allowed"

        for i in enumerate(config.compared_options):
            index = i[0]
            name = i[1]
            val = config.compared_options.get(name)
            no = False

            for _name in tabu:
                if name.startswith(_name):
                    no = True

            if no == True:
                continue

            val.data["name"] = name
            val.data["current"] = config.options.get(name)

            result.append(val.out())

        return result
