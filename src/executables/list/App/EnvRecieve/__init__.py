from executables.acts import Act
from resources.Consts import consts
from app.App import config, env

class Implementation(Act):
    async def execute(self, args = {}):
        assert config.get("web.env_editing.allow") == True, "env editing is not allowed"

        return env.options
