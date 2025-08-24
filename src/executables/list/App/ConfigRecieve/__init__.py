from executables.acts import Act
from resources.Consts import consts
from app.App import config

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return config.get("web.config_editing.allow")

        return super().canBeUsedAt(at)

    async def execute(self, args = {}):
        result = []

        for name, itm in config.compared_options.items():
            val = config.compared_options.get(name)
            no = False

            for _name in consts.get("config.hidden_values_spaces"):
                if name.startswith(_name):
                    no = True

            if no == True:
                continue

            val.configuration["name"] = name
            val.configuration["current"] = config.options.get(name)

            result.append(val.describe())

        return result
