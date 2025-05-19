from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Entity import Entity

class RemoveEntity(BaseAct):
    name = 'RemoveEntity'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'id' not in self.passed_params:
            raise NotPassedException("--entity_id not passed")

        entity_id = self.passed_params.get("entity_id")
        delete_file = int(self.passed_params.get("delete_file", "0")) == 1
        if delete_file == None:
            delete_file = False

        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")
        
        entity.delete(delete_file=delete_file)

        return 1
