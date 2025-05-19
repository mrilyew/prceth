from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from resources.Exceptions import NotPassedException, NotFoundException

class GetItemsCountInCollection(BaseAct):
    name = 'GetItemsCountInCollection'
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
    
        collection_id = self.passed_params.get("collection_id")
        query = self.passed_params.get("query")
        columns_search = self.passed_params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection.getItemsCount(query=query,columns_search=columns_search)
