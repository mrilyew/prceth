from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json, often_params
from executables.services.Base.Base import BaseService

class RSS(BaseService):
    name = 'RSS'
    category = 'Common'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        url = self.config.get("url")
