from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from resources.Exceptions import NotPassedException, NotFoundException

class GetCollectionById(BaseAct):
    name = 'GetCollectionById'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if "collection_id" not in self.passed_params:
            raise NotPassedException("--collection_id not passed")

        collection_id = self.passed_params.get("collection_id")
        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")

        return collection
