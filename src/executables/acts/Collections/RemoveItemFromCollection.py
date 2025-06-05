from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.ContentUnit import ContentUnit
from db.Collection import Collection

class RemoveItemFromCollection(BaseAct):
    name = 'RemoveItemFromCollection'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'collection_id' not in self.passed_params and 'ContentUnit_id' not in self.passed_params:
            raise NotPassedException("collection_id and ContentUnit_id are not passed")
        
        collection_id = self.passed_params.get("collection_id")
        ContentUnit_id = self.passed_params.get("ContentUnit_id")
        delete_ContentUnit = self.passed_params.get("delete_ContentUnit")
        if delete_ContentUnit == None:
            delete_ContentUnit = False
        
        collection = Collection.get(collection_id)
        ContentUnit = ContentUnit.get(ContentUnit_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        if ContentUnit == None:
            raise NotFoundException("ContentUnit not found")
        
        collection.removeItem(ContentUnit, delete_ContentUnit=delete_ContentUnit)

        return 1
