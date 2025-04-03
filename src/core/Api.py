from resources.Globals import config, time, ExtractorsRepository, ActsRepository, ServicesRepository, logger, json, file_manager, Path, storage, utils
from resources.Exceptions import NotFoundException, NotPassedException, ExtractorException
from db.Collection import Collection
from db.Entity import Entity
from db.File import File

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
        
        collection.delete_instance()
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
    def getCollectionById(self, params): # todo multiselect
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

        return entity
    def getEntityById(self, params):
        if 'ids' not in params:
            raise NotPassedException("--ids not passed")
        
        ids = params.get("ids").split(",")
        entities = Entity.get(ids)
        if entities == None or len(entities) < 1:
            raise NotFoundException("Entity not found")
        
        return entities
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
    async def uploadEntity(self, __INPUT_ARGS):
        if 'extractor' not in __INPUT_ARGS:
            raise NotPassedException('--extractor not passed')
        
        __extractor_input_name = __INPUT_ARGS.get("extractor") # Extractor that will be using for export
        collection_id = __INPUT_ARGS.get("collection_id", None) # Collection id to where entity will added
        # None: Result will be saved as entity
        # Text: Result will be saved at another dir
        __export_folder = __INPUT_ARGS.get("export_to_dir", None)
        __export_to_db = __export_folder == None
        __custom_temp_dir = __INPUT_ARGS.get("custom_temp_dir", None)
        
        col = None
        INSTANCE_CLASS = (ExtractorsRepository()).getByName(extractor_name=__extractor_input_name)
        assert INSTANCE_CLASS != None, "Extractor not found"

        EXTRACTOR_INSTANCE = INSTANCE_CLASS(temp_dir=__custom_temp_dir,del_dir_on_fail=__export_to_db == True,need_preview=__export_to_db == True)
        EXTRACTOR_INSTANCE.setArgs(__INPUT_ARGS)
        EXTRACTOR_RESULTS = None
        try:
            EXTRACTOR_RESULTS = await EXTRACTOR_INSTANCE.execute(__INPUT_ARGS)
            if EXTRACTOR_RESULTS == None:
                raise Exception("Nothing returned")
        except Exception as __ee:
            logger.log(message=f"Extractor {__extractor_input_name} returned error: {str(__ee)}",noConsole=True)
            raise __ee
        
        ENTITIES_COUNT = len(EXTRACTOR_RESULTS.get("entities"))
        if ENTITIES_COUNT < 1:
            raise ExtractorException("nothing exported")

        RETURN_ENTITIES = []
        for ENTITY in EXTRACTOR_RESULTS.get("entities"):
            RETURN_ENTITIES.append(ENTITY)
            for _ENTITY in ENTITY.getLinkedEntities():
                RETURN_ENTITIES.append(_ENTITY)
        
        for MOVE_ENTITY in RETURN_ENTITIES:
            if MOVE_ENTITY.file != None:
                MOVE_ENTITY.file.moveTempDir()
        
        if EXTRACTOR_RESULTS.get("collection") != None:
            RETURN_ENTITIES = []
            col = EXTRACTOR_INSTANCE._collectionFromJson(EXTRACTOR_RESULTS.get("collection"))
            for i_entity in EXTRACTOR_RESULTS.get("entities"):
                col.addItem(i_entity)

            RETURN_ENTITIES.append(col)

        if collection_id != None:
            POST_COLLECTION = Collection.get(collection_id)
            if POST_COLLECTION == None:
                logger.log(section="App", name="Entity Uploader", message="Collection not found, not adding.")
            else:
                for _ENT in RETURN_ENTITIES:
                    POST_COLLECTION.addItem(_ENT)

        await EXTRACTOR_INSTANCE.postRun()
        if __export_folder != None:
            if col != None:
                __act = (ActsRepository().getByName("Export.CollectionToFS"))()
                __act.execute(i=col.id,args={"dir": __export_folder})
            else:
                items_id = []
                for __e in EXTRACTOR_RESULTS.get("entities"):
                    items_id.append(str(__e.id))
                
                __act = (ActsRepository().getByName("Export.EntityToFS"))()
                __act.execute(i=",".join(items_id),args={"dir": __export_folder})

        return RETURN_ENTITIES
        
    def getExtractors(self, params):
        show_hidden = int(params.get("show_hidden", "0")) == 1

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

