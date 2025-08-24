from executables.acts import Act
from resources.Consts import consts
from app.App import config, env

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return config.get("web.env_editing.allow")

        return super().canBeUsedAt(at)

    async def execute(self, args = {}):
        return env.options
