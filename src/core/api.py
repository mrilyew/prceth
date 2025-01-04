from resources.globals import config, time
from resources.exceptions import NotFoundException
from db.collection import Collection
from db.entity import Entity

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
    def getCollectionById(self, params):
        collection_id = params.get("collection_id")
        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection
    def getItemsInCollection(self, params):
        collection_id = params.get("collection_id")
        query = params.get("query")
        offset = params.get("offset", 0)
        count = params.get("count", 10)
        columns_search = params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        items = collection.getItems(offset=offset,limit=count,query=query,columns_search=columns_search)
        
        return items
    def getItemsCountInCollection(self, params):
        collection_id = params.get("collection_id")
        query = params.get("query")
        columns_search = params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection.getItemsCount(query=query,columns_search=columns_search)
    def addItemToCollection(self, params):
        collection_id = params.get("collection_id")
        entity_id = params.get("entity_id")

        collection = Collection.get(collection_id)
        entity = Entity.get(entity_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        if entity == None:
            raise NotFoundException("Entity not found")
        
        collection.addItem(entity)
    def removeItemFromCollection(self, params):
        collection_id = params.get("collection_id")
        entity_id = params.get("entity_id")
        delete_entity = params.get("delete_entity")
        if delete_entity == None:
            delete_entity = False
        
        collection = Collection.get(collection_id)
        entity = Entity.get(entity_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        if entity == None:
            raise NotFoundException("Entity not found")
        
        collection.removeItem(entity, delete_entity=delete_entity)
    def removeEntity(self, params):
        entity_id = params.get("entity_id")
        delete_file = params.get("delete_file")
        if delete_file == None:
            delete_file = False
        
        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")
        
        entity.delete(delete_file=delete_file)
    def editEntity(self, params):
        entity_id = params.get("entity_id")
        display_name = params.get("display_name")
        description = params.get("description")

        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")

        if display_name != None:
            entity.display_name = display_name
        if description != None:
            entity.description = description

        entity.edited_at = time.time()
        entity.save()
    def getEntityById(self, params):
        entity_id = params.get("entity_id")
        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")
        
        return entity
    def getGlobalEntities(self, params):
        query = params.get("query")
        if query == None:
            query = ""
        
        offset = params.get("offset", 0)
        count = params.get("count", 10)
        columns_search = params.get("columns_search")

        fetch = Entity.fetchItems(query=query,columns_search=columns_search)
        items = fetch.offset(offset).limit(count)
        count = fetch.count()

        return items, count

api = Api()
