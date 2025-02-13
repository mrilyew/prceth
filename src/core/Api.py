from resources.Globals import config, time, utils, logger, json, file_manager, Path
from resources.Exceptions import NotFoundException, NotPassedException
from db.Collection import Collection
from db.Entity import Entity
from core.Wheels import extractor_wheel, extractor_list, acts_wheel, acts_list, service_wheel, services_list

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
        preview_entity = None
        add_after = None

        if "name" not in params or len(params.get("name")) == 0:
            raise NotPassedException("name is not passed")
        
        if "preview_id" in params:
            __preview_entity = Entity.get(int(params.get("preview_id")))
            if __preview_entity != None:
                preview_entity = __preview_entity
        
        if "to_add" in params:
            __add_collection = Collection.get(int(params.get("to_add")))
            if __add_collection != None:
                add_after = __add_collection
        
        col = Collection()
        col.name = params.get("name")
        col.description = params.get("description")
        col.tags = params.get("tags")
        if params.get('frontend_data') != None:
            col.frontend_data = params.get('frontend_data')

        if preview_entity != None:
            col.preview_id = preview_entity.id
        
        col.order = Collection.getAllCount()
        if add_after != None:
            col.unlisted = 1
        
        col.save(force_insert=True)
        if add_after != None:
            add_after.addItem(col)

        return col
    def editCollection(self, params):
        preview_entity = None
        if params.get('collection_id', None) == None:
            raise NotPassedException("collection_id not passed")
        
        col = Collection.get(int(params.get('collection_id')))
        if col == None:
            raise NotFoundException("Collection not found")
        
        if "preview_id" in params:
            __preview_entity = Entity.get(int(params.get("preview_id")))
            if __preview_entity != None:
                preview_entity = __preview_entity
        
        if 'name' in params and len(params.get("name")) > 0:
            col.name = params.get('name')
        if 'description' in params:
            col.description = params.get('description')
        if 'frontend_data' in params:
            col.frontend_data = params.get('frontend_data')
        if preview_entity != None:
            col.preview_id = preview_entity.id
        
        col.edited_at = time.time()
        col.save()
        
        return col
    def deleteCollection(self, params):
        if not params.get("collection_id"):
            raise NotPassedException("collection_id not passed")
        
        collection = Collection.get(params.get('collection_id'))
        if collection == None:
            raise NotFoundException("Collection not found")
        
        collection.delete()
        return True
    def switchCollections(self, params):
        if 'id1' not in params and 'id2' not in params:
            raise NotPassedException("id1 and id2 are not passed")

        collection_1 = Collection.get(params.get('id1'))
        collection_2 = Collection.get(params.get('id2'))
        if collection_1 != None and collection_2 != None:
            collection_1.switch(collection_2)
        else:
            raise NotFoundException("Collections are not found")
    def getCollectionById(self, params):
        if "collection_id" not in params:
            raise NotPassedException("--collection_id not passed")
        
        collection_id = params.get("collection_id")
        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection
    def getAllCollections(self, params):
        query  = params.get("query")
        offset = params.get("offset", 0)
        count  = params.get("count", 10)
        collections = Collection.getAll(query)
        collections = collections.limit(count).offset(offset)

        return collections, Collection.getAllCount(query)
    def getItemsInCollection(self, params):
        if 'collection_id' not in params:
            raise NotPassedException('Error: "--collection_id" not passed')
        
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if params.get("search_by_" + column) != None:
                columns_search.append(column)

        collection_id = int(params.get("collection_id"))
        query = params.get("query")
        offset = int(params.get("offset", 0))
        count = int(params.get("count", 10))

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        items = collection.getItems(offset=offset,limit=count,query=query,columns_search=columns_search)
        
        return items
    def getItemsCountInCollection(self, params):
        if 'collection_id' not in params:
            raise NotPassedException('Error: "--collection_id" not passed')

        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if params.get("search_by_" + column) != None:
                columns_search.append(column)
    
        collection_id = params.get("collection_id")
        query = params.get("query")
        columns_search = params.get("columns_search")

        collection = Collection.get(collection_id)
        if collection == None:
            raise NotFoundException("Collection not found")
        
        return collection.getItemsCount(query=query,columns_search=columns_search)
    def addItemToCollection(self, params):
        if 'collection_id' not in params and 'entity_id' not in params:
            raise NotPassedException("collection_id and entity_id are not passed")
        
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
        if 'collection_id' not in params and 'entity_id' not in params:
            raise NotPassedException("collection_id and entity_id are not passed")
        
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
        if 'id' not in params:
            raise NotPassedException("--entity_id not passed")
        
        entity_id = params.get("entity_id")
        delete_file = int(params.get("delete_file", "0")) == 1
        if delete_file == None:
            delete_file = False
        
        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")
        
        entity.delete(delete_file=delete_file)
    def editEntity(self, params):
        if 'entity_id' not in params:
            raise NotPassedException('--entity_id not passed')
        
        entity_id = int(params.get("entity_id"))
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
        if 'entity_id' not in params:
            raise NotPassedException("--entity_id not passed")
        
        entity_id = int(params.get("entity_id"))
        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")
        
        return entity
    def getGlobalEntities(self, params):
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if params.get("search_by_" + column) != None:
                columns_search.append(column)
        
        query = params.get("query")
        if query == None:
            query = ""
        
        offset = int(params.get("offset", 0))
        count = int(params.get("count", 10))
        columns_search = params.get("columns_search")

        fetch = Entity.fetchItems(query=query,columns_search=columns_search)
        items = fetch.offset(offset).limit(count)
        count = fetch.count()

        return items, count
    async def uploadEntity(self, params):
        # TODO переписать превью в отдельную директорию с хешами
        # + хеш для entity вместо id
        if 'extractor' not in params:
            raise NotPassedException('--extractor not passed')

        # Extractor that will be using for export
        extractor_input_name = params.get("extractor")
        # Collection to where entity will added
        collection_id = params.get("collection_id", None)
        # Display entity name
        display_name = params.get("display_name")
        # Alt
        description = params.get("description")
        # None: Result will be saved as entity
        # Text: Result will be saved at another dir
        export_as_entity = params.get("export_to_folder", None) == None
        temp_dir = None
        if export_as_entity == True:
            temp_dir = utils.generate_temp_entity_dir()
        else:
            temp_dir = params.get("export_to_folder")
            if Path(temp_dir).is_dir() == False:
                raise NotADirectoryError("Directory not found")

        instance, results = await extractor_wheel(args=params,entity_dir=temp_dir,extractor_name=extractor_input_name)
        if export_as_entity == False: 
            return temp_dir

        entity = Entity()

        entity.format = results.format
        entity.original_name = results.original_name
        entity.filesize = results.filesize
        entity.dir_filesize = file_manager.getFolderSize(temp_dir)
        entity.extractor_name = extractor_input_name
        if display_name != None:
            entity.display_name = display_name
        else:
            entity.display_name = results.original_name
        if description != None:
            entity.description = description
        if results.hasSource():
            entity.source = results.source
        if results.hasJsonInfo():
            json_ = results.json_info
            entity.json_info = json.dumps(json_)
            entity.index_content = str(utils.json_values_to_string(json_)).replace('None', '').replace('  ', ' ')
        
        entity.save()
        instance.cleanup(entity=entity)
        
        thumb_result = instance.thumbnail(entity=entity,args=results)
        if thumb_result != None:
            entity.preview = ",".join(thumb_result["previews"])

        if collection_id != None:
            collection = Collection.get(collection_id)
            if collection == None:
                logger.log("App", "Entity Uploader", "Collection not found, not adding.")
            else:
                collection.addItem(entity)

        return entity
    def getExtractors(self, params):
        show_hidden = params.get("show_hidden", False) == True

        extractors = extractor_list(show_hidden=show_hidden)

        return extractors
    def getActs(self, params):
        __show_hidden = params.get("show_hidden", None) != None
        __search_type = params.get("search_type", "all")

        acts = acts_list(search_type=__search_type,show_hidden=__show_hidden)

        return acts
    def runAct(self, params):
        if "act_name" not in params:
            raise NotPassedException('--act_name not passed')

        act_name = params.get("act_name")
        instance, results = acts_wheel(args=params,entity_dir="",act_name=act_name)

        instance.cleanup()
        return results
    def getServices(self, params):
        services = services_list(show_hidden=(int(params.get("show_hidden", 0)) == 1))

        return services
    def runService(self, params):
        if 'service_name' not in params:
            raise NotPassedException('--service_name not passed')

        service_name = params.get("service_name")
        if service_name == None:
            raise ValueError("--service_name is not passed")

        service_wheel(args=params,service_name=service_name)

        return True

api = Api()
