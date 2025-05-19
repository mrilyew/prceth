from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from resources.Exceptions import NotPassedException, NotFoundException

class GetItemsInCollection(BaseAct):
    name = 'GetItemsInCollection'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'collection_id' not in self.passed_params:
            raise NotPassedException('Error: "--collection_id" not passed')
        
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if self.passed_params.get("search_by_" + column) != None:
                columns_search.append(column)

        collection_id = int(self.passed_params.get("collection_id"))
        query = self.passed_params.get("query")
        offset = int(self.passed_params.get("offset", 0))
        count = int(self.passed_params.get("count", 10))

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        items = collection.getItems(offset=offset,limit=count,query=query,columns_search=columns_search)
        
        return items
