from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Entity import Entity
from db.Collection import Collection

class RemoveItemFromCollection(BaseAct):
    name = 'RemoveItemFromCollection'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'collection_id' not in self.passed_params and 'entity_id' not in self.passed_params:
            raise NotPassedException("collection_id and entity_id are not passed")
        
        collection_id = self.passed_params.get("collection_id")
        entity_id = self.passed_params.get("entity_id")
        delete_entity = self.passed_params.get("delete_entity")
        if delete_entity == None:
            delete_entity = False
        
        collection = Collection.get(collection_id)
        entity = Entity.get(entity_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        if entity == None:
            raise NotFoundException("Entity not found")
        
        collection.removeItem(entity, delete_entity=delete_entity)

        return 1
