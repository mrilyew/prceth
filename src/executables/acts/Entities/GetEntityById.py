from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Entity import Entity

class GetEntityById(BaseAct):
    name = 'GetEntityById'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'ids' not in self.passed_params:
            raise NotPassedException("--ids not passed")
        
        ids = self.passed_params.get("ids").split(",")
        entities = Entity.get(ids)
        if entities == None or len(entities) < 1:
            raise NotFoundException("Entity not found")
        
        return entities
