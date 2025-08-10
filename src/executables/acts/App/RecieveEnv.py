from executables.acts import BaseAct
from resources.Consts import consts
from app.App import config, env

class RecieveEnv(BaseAct):
    async def execute(self, args = {}):
        assert config.get("web.env_editing.allow") == True, "env editing is not allowed"

        return env.options
