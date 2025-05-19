from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from resources.Exceptions import NotPassedException, NotFoundException

class SwitchCollections(BaseAct):
    name = 'SwitchCollections'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'id1' not in self.passed_params and 'id2' not in self.passed_params:
            raise NotPassedException("id1 and id2 are not passed")

        collection_1 = Collection.get(self.passed_params.get('id1'))
        collection_2 = Collection.get(self.passed_params.get('id2'))
        if collection_1 != None and collection_2 != None:
            collection_1.switch(collection_2)
        else:
            raise NotFoundException("Collections are not found")

        return 1
