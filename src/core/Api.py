from resources.Globals import config, time, ExtractorsRepository, ActsRepository, ServicesRepository, logger, json, file_manager, Path, storage
from resources.Exceptions import NotFoundException, NotPassedException
from db.Collection import Collection
from db.Entity import Entity

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

        fetch = Entity.fetchItems(query=query,columns_search=columns_search)
        items = fetch.offset(offset).limit(count)
        count = fetch.count()

        return items, count
    async def uploadEntity(self, _ARGS):
        if 'extractor' not in _ARGS:
            raise NotPassedException('--extractor not passed')

        # Extractor that will be using for export
        __extractor_input_name = _ARGS.get("extractor")
        # Collection to where entity will added
        collection_id = _ARGS.get("collection_id", None)
        # None: Result will be saved as entity
        # Text: Result will be saved at another dir
        __export_as_entity = _ARGS.get("export_to_folder", None) == None

        EXPORT_DIRECTORY = None
        if __export_as_entity == True:
            EXPORT_DIRECTORY = storage.makeTemporaryCollectionDir()
        else:
            EXPORT_DIRECTORY = _ARGS.get("export_to_folder")
            if Path(EXPORT_DIRECTORY).is_dir() == False:
                raise NotADirectoryError("Directory not found")
        
        INSTANCE_CLASS = (ExtractorsRepository()).getByName(extractor_name=__extractor_input_name)
        assert INSTANCE_CLASS != None, "Extractor not found"

        EXTRACTOR_INSTANCE = INSTANCE_CLASS(temp_dir=EXPORT_DIRECTORY)
        EXTRACTOR_RESULTS = await EXTRACTOR_INSTANCE.shortExecute(_ARGS)
        
        if __export_as_entity == True: 
            RETURN_ENTITY = EXTRACTOR_INSTANCE.saveAsEntity(EXTRACTOR_RESULTS)
            if RETURN_ENTITY.type == 0:
                EXTRACTOR_INSTANCE.moveDestinationDirectory(entity=RETURN_ENTITY)
            
            thumb_result = EXTRACTOR_INSTANCE.thumbnail(entity=RETURN_ENTITY,args=EXTRACTOR_RESULTS)
            if thumb_result != None:
                RETURN_ENTITY.preview = json.dumps(thumb_result)
                RETURN_ENTITY.save()

            if collection_id != None:
                collection = Collection.get(collection_id)
                if collection == None:
                    logger.log("App", "Entity Uploader", "Collection not found, not adding.")
                else:
                    collection.addItem(RETURN_ENTITY)

            await EXTRACTOR_INSTANCE.postRun()
            return RETURN_ENTITY
        else:
            RETURN_ENTITY = EXTRACTOR_INSTANCE.saveToDirectory(EXTRACTOR_RESULTS) # Does nothing :D
            return
        
    def getExtractors(self, params):
        show_hidden = params.get("show_hidden", False) == True

        extractors = (ExtractorsRepository()).getList(show_hidden=show_hidden)

        return extractors
    def getActs(self, params):
        __show_hidden = params.get("show_hidden", None) != None
        __search_type = params.get("search_type", "all")

        acts = ActsRepository().getList(search_type=__search_type,show_hidden=__show_hidden)

        return acts
    def runAct(self, params):
        assert "name" in params, "name not passed"

        __act_name = params.get("name")
        __act_main = params.get("i")
        __act_res = ActsRepository().getByName(act_name=__act_name)
        assert __act_res != None, "act not found"

        OUT_ACT = __act_res()
        ACT_MAIN_INPUT = OUT_ACT.parseMainInput(main_input=__act_main)
        if ACT_MAIN_INPUT == None:
            raise NotFoundException("entity/collection/string not found")

        ACT_F = OUT_ACT.execute(args=params,i=ACT_MAIN_INPUT)

        return {"results": ACT_F}
    def getServices(self, params):
        services = (ServicesRepository()).getList(show_hidden=(int(params.get("show_hidden", 0)) == 1))

        return services
    def runService(self, params):
        if 'service_name' not in params:
            raise NotPassedException('--service_name not passed')

        service_name = params.get("service_name")
        if service_name == None:
            raise ValueError("--service_name is not passed")

        (ServicesRepository()).run(args=params,service_name=service_name)

        return True

api = Api()
