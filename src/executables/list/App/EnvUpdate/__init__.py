from declarable.Arguments import ObjectArgument, LimitedArgument
from executables.acts import Act
from resources.Consts import consts
from app.App import config, env

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["values"] = ObjectArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return config.get("web.env_editing.allow")

        return super().canBeUsedAt(at)

    async def execute(self, args = {}):
        values = args.get("values")

        assert values != None, "new values not passed"

        for name, itm in values.items():
            val = values.get(name)
            no = False

            if val == None:
                continue

            env.set(name, val)

        return {
            "success": True
        }
