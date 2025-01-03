from resources.globals import config, time
from resources.exceptions import NotFoundException
from db.collection import Collection

class Api():
    def __init__(self):
        self.ctx = "cli"
    def setOption(self, option_name, option_value):
        config.set(option_name, option_value)
        return True
    def getOption(self, option_name):
        return config.get(option_name)
    def resetOptions(self):
        return config.reset()
    def getAllOptions(self):
        return config.data
    def createCollection(self, params):
        params["order"] = Collection.getAllCount()
        
        col = Collection()
        col.name = params.get("name")
        col.description = params.get("description")
        if params.get('frontend_type') != None:
            col.frontend_type = params.get('frontend_type')

        if params.get('icon_hash') != None:
            col.icon_hash = params.get('icon_hash')
        
        col.order = Collection.getAllCount()
        if params.get('to_add') != None:
            col.hidden = 1
        
        col.save(force_insert=True)
        if params.get('to_add') != None:
            params.get('to_add').addItem(col)

        return col
    def editCollection(self, params):
        col = Collection.get(params.get('collection_id'))
        if col == None:
            raise NotFoundException("Collection not found")
        
        if 'name' in params:
            col.name = params.get('name')
        if 'description' in params:
            col.description = params.get('description')
        if 'frontend_type' in params:
            col.frontend_type = params.get('frontend_type')
        if 'icon_hash' in params:
            col.icon_hash = params.get('icon_hash')
        
        col.edited_at = time.time()
        col.save()
        
        return col
    def deleteCollection(self, params):
        col = Collection.get(params.get('collection_id'))
        if col == None:
            raise NotFoundException("Collection not found")
        
        col.delete_instance(recursive=True)
        return True
    def switchCollections(self, params):
        collection_1 = Collection.get(params.get('id1'))
        collection_2 = Collection.get(params.get('id2'))
        if collection_1 != None and collection_2 != None:
            collection_1.switch(collection_2)
        else:
            raise NotFoundException("Collections not found")
    def getItemsInCollection(self, params):
        collection_id = params["collection_id"]
        query = params.get("query")
        offset = params.get("offset")
        count = params.get("count")
        columns_search = params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        items = collection.getItems(offset=offset,limit=count,query=query,columns_search=columns_search)
        
        return items
    def getItemsCountInCollection(self, params):
        collection_id = params["collection_id"]
        query = params.get("query")
        columns_search = params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection.getItemsCount(query=query,columns_search=columns_search)

api = Api()
