from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection

class GetAllCollections(BaseAct):
    name = 'GetAllCollections'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        query  = self.passed_params.get("query")
        offset = self.passed_params.get("offset", 0)
        count  = self.passed_params.get("count", 10)
        collections = Collection.getAll(query)
        collections = collections.limit(count).offset(offset)

        total_count = Collection.getAllCount(query)

        return total_count
