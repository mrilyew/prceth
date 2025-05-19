from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Collection import Collection

class DeleteCollection(BaseAct):
    name = 'DeleteCollection'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if not self.passed_params.get("collection_id"):
            raise NotPassedException("collection_id not passed")
        
        collection = Collection.get(self.passed_params.get('collection_id'))
        if collection == None:
            raise NotFoundException("Collection not found")
        
        collection.delete_instance()
