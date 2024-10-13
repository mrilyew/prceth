from resources.globals import time, platform, traceback, Path, utils, db, Collection, Entity, Relation, settings, file_manager, consts, load_plugins

args = utils.parse_args()

match args.get('act'):
    case None:
        print('"--act" not passed.')
    
    # SETTINGS

    case "settings.get":
        if 'param' in args:
            print(settings.get(args['param']))
        else:
            print('\'--param\' not passed.')
    
    case "settings.set":
        if 'param' in args and 'value' in args:
            settings.set(args.get('param'), args['value'])
        else:
            print('\'--param\' and \'--value\' are not passed.')
    
    case "settings.reset":
        settings.reset()
        print('Settings was reset.')

    # COLLECTIONS

    case "collections.get":
        for col in Collection.getAll():
            print(str(col.takeInfo()))
    case "collections.getCount":
        print(Collection.getAllCount())
    case 'collections.create':
        if 'name' not in args:
            print('Error: "--name" not passed')
            exit()

        col = Collection()
        col.name = args.get('name')
        col.description = args.get('description')

        if args.get('innertype') != None:
            col.innertype = args.get('innertype')

        if args.get('icon_hash') != None:
            col.icon_hash = args.get('icon_hash')
        
        col.order = Collection.getAllCount()
        if args.get('add_after') != None:
            col.hidden = 1
        
        col.save(force_insert=True)

        if args.get('add_after') != None:
            to_add = Collection.get(args.get('add_after'))
            if to_add == None:
                print('Invalid collection')
                exit(-1)
            
            to_add.addItem(col)
        
        print(col.takeInfo())
    case 'collections.getById':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit()

        collection = Collection.get(args.get('id'))
        if collection != None:
            print(collection.takeInfo())
        else:
            print("Not found")
    case 'collections.edit':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit()

        collection = Collection.get(args.get('id'))
        if collection != None:
            if 'name' in args:
                collection.name = args.get('name')

            if 'description' in args:
                collection.description = args.get('description')
                                
            if 'innertype' in args:
                collection.innertype = args.get('innertype')
                                                        
            if 'icon_hash' in args:
                collection.icon_hash = args.get('icon_hash')

            collection.edited_at = time.time()
            collection.save()
            print(collection.takeInfo())
        else:
            print("Not found")
    case 'collections.delete':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit()

        collection = Collection.get(args.get('id'))
        if collection != None:
            collection.delete_instance(recursive=True)
        else:
            print("Not found")        
    case 'collections.switch':
        if 'id1' not in args and 'id2' not in args:
            print('Error: "--id1" and "--id2" are not passed')
            exit()

        collection_1 = Collection.get(args.get('id1'))
        collection_2 = Collection.get(args.get('id2'))

        if collection_1 != None and collection_2 != None:
            collection_1.switch(collection_2)
        else:
            print("Not found")
    case 'collections.getItems':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit()

        collection = Collection.get(args.get('id'))
        if collection != None:
            columns_search = ['original_name', 'display_name']
            if int(args.get('search_by_description') or 0) == 1:
                columns_search.append('description')
            
            if int(args.get('search_by_source') or 0) == 1:
                columns_search.append('source')
            
            if int(args.get('search_by_index_info') or 0) == 1:
                columns_search.append('index_info')

            if int(args.get('search_by_saved_via') or 0) == 1:
                columns_search.append('saved_via')

            if int(args.get('search_by_author') or 0) == 1:
                columns_search.append('author')

            items = collection.getItems(page=args.get('page'), query=args.get('query'), columns_search=columns_search)

            for col in items:
                print(str(col.takeInfo()))
        else:
            print("Not found")
    
    case 'collections.getItemsCount':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit()

        collection = Collection.get(args.get('id'))
        if collection != None:
            search_options = {
                "query": args.get('query'),
                "name_search": int(args.get('name_search') if args.get('name_search') else 0),
                "description_search": int(args.get('description_search') if args.get('description_search') else 0)
            }

            print(collection.getItemsCount(query_options=search_options))
        else:
            print("Not found")
    
    case 'collections.append':
        if 'collection_id' not in args and 'entity_id' not in args:
            print('Error: "--collection_id" and "--entity_id" are not passed')
            exit()

        id = args.get('entity_id')
        collection = Collection.get(args.get('collection_id'))
        entity = Entity.get(id)

        if collection == None or entity == None:
            print("Not found")
            exit()

        try:
            collection.addItem(entity)
        except ValueError:
            print("Error: Entity does not belows to collection")
    
    # ENTITIES

    case 'entities.globalSearch':
        if 'query' not in args:
            print('Error: "--query" not passed')
            exit()
        
        columns_search = ['original_name', 'display_name']
        if int(args.get('search_by_description') or 0) == 1:
            columns_search.append('description')
        
        if int(args.get('search_by_source') or 0) == 1:
            columns_search.append('source')
        
        if int(args.get('search_by_index_info') or 0) == 1:
            columns_search.append('index_info')

        if int(args.get('search_by_saved_via') or 0) == 1:
            columns_search.append('saved_via')

        if int(args.get('search_by_author') or 0) == 1:
            columns_search.append('author')
        
        search = Entity.search(page=args.get('page'), query=args.get('query'), columns_search=columns_search)
        for col in search:
            print(str(col.takeInfo()))
    case 'entities.remove':
        if 'collection_id' not in args or 'entity_id' not in args:
            print('Error: "--collection_id" and "--entity_id" are not passed')
            exit()

        collection = Collection.get(args.get('collection_id'))
        entity = Entity.get(args.get('entity_id'))

        if collection != None and entity != None:
            try:
                collection.removeItem(entity=entity,delete_entity=True)
            except ValueError as e:
                print(e)
        else:
            print("Not found")

    case 'entities.create':
        if 'collection_id' not in args:
            print('Pass "collection_id" to upload')
            exit()

        collection = Collection.get(args.get('collection_id'))
        if 'method' not in args:
            print('"--method" not passed')
            exit()
        
        method = args.get('method')
        plugins = load_plugins('upload_plugins')
        instance = None
        temp_dir = utils.generate_temp_entity_dir()

        try:
            instance = plugins[method](temp_dir=temp_dir)
        except KeyError:
            print('Plugin not found')
            exit()

        try:
            results = instance.run(args=args)
        except Exception as e:
            traceback.print_exc()
            instance.cleanup_fail()
            exit()
        
        entity = Entity()

        entity.format = str(results.get('format'))
        entity.original_name = results.get('original_name')
        entity.filesize = results.get('filesize')
        entity.saved_via = instance.name

        if 'source' in results:
            entity.source = results.get('source')
        
        if 'cached_content' in results:
            entity.cached_content = results.get('cached_content')

        if 'index_info' in results:
            entity.index_info = results.get('index_info').replace('None', '').replace('  ', ' ')

        if 'color' in args:
            entity.color = str(args.get('color'))
        else:
            if 'color' in results:
                entity.color = str(results.get('color'))
        
        if 'pinned' in args:
            pinned = 0
            if int(args.get('pinned')) == 1:
                pinned = 1
            
            entity.pinned = pinned
        
        if 'display_name' in args:
            entity.display_name = args.get('display_name')
        else:
            entity.display_name = entity.original_name

        if 'description' in args:
            entity.description = args.get('description')
        
        entity.save()
        instance.cleanup(entity=entity)
        collection.addItem(entity)

        print(entity.takeInfo())
    case 'entities.edit':
        if 'id' not in args:
            print('"--id" was not passed')
            exit()

        entity = Entity.get(args.get('id'))
        if args.get('name') != None:
            entity.display_name = args.get('name')
        
        if args.get('description') != None:
            entity.description = args.get('description')
             
        if args.get('innertype') != None:
            entity.innertype = args.get('innertype')

        if args.get('icon_hash') != None:
            entity.icon_hash = args.get('icon_hash')

        entity.edited_at = time.time()
        entity.save()
    case 'entities.changeCollection':
        if 'new_collection_id' not in args or 'entity_id' not in args:
            print('"new_collection_id" and "entity_id" are not passed')
            exit()

        collection = Collection.get(args.get('new_collection_id'))
        if collection == None:
            print('Invalid collection')
            exit(-1)
        
        entity = Entity.get(args.get('entity_id'))
        if entity == None:
            print('Invalid entity')
            exit(-1)
        
        Relation.delete().where(Relation.child_entity == entity.id).execute()
        collection.addItem(entity)
    
    # PLUGINS

    case 'plugins.get':
        folder = args.get('folder')
        plugins = load_plugins(folder=folder)
        for plugin in plugins:
            plugin_class = plugins.get(plugin)()
            print(plugin_class.getDesc())
    
    case 'plugins.getActionsForEntity':
        if 'mid' not in args:
            print('Pass "mid" like "[type]_[id]"')
            exit()
        
        type, id = tuple(args.get('mid').split('_'))
        plugins = load_plugins('action_plugins')
        entity = None
        if type == "collection":
            entity = Collection.get(id)
        elif type == 'entity':
            entity = Entity.get(id)

        if entity == None:
            print('No entity')
            exit()
        
        final_plugins = []
        for plug in plugins:
            plugin = plugins[plug]()
            if plugin.canRun(entity):
                final_plugins.append(plugin)

        for plugin in final_plugins: 
            print(plugin.getDesc())
    
    case 'plugins.runAction':
        if 'mid' not in args:
            print('Pass "mid" like "[type]_[id]"')
            exit()

        if 'plugin' not in args:
            print('"plugin" was not passed')
            exit()
        
        plugin = args.get('plugin')
        plugins = load_plugins('action_plugins')
        type, id = tuple(args.get('mid').split('_'))

        entity = None
        if type == "collection":
            entity = Collection.get(id)
        elif type == 'entity':
            entity = Entity.get(id)

        class_plugin = plugins.get(plugin)
        if class_plugin == None:
            print("Plugin was not found")
            exit()

        class_plugin_ex = class_plugin()
        if class_plugin_ex.canRun(input_entity=entity) == False:
            print('Plugin cannot be runned on this')
            exit()
        
        print(class_plugin_ex.run(input_entity=entity,args=args))
    
    case 'plugins.runBase':
        if 'plugin' not in args:
            print('"plugin" was not passed')
            exit()
        
        plugin = args.get('plugin')
        plugins = load_plugins('base_plugins')
        class_plugin = plugins.get(plugin)
        if class_plugin == None:
            print("Plugin was not found")
            exit()

        class_plugin_ex = class_plugin()
        res = class_plugin_ex.run(args=args)

        if hasattr(res, '__len__'):
            for item in res:
                print(str(item) + '\n')
        else:
            print(res)
    case 'plugins.runService':
        if 'service' not in args:
            print('"service" was not passed')
            exit()

        service_name = args.get('service')
        input_data = args.get('input_data')
        plugins = load_plugins('services_plugins')
        service = plugins.get(service_name)
        if service == None:
            print("Service was not found")
            exit()

        service_ex = service()
        service_ex.start(args=args)
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            service_ex.stop()
        pass
    case 'log':
        from core.logger import logger
        logger.log(args.get('section'), args.get('name'), args.get('message'))
    case _:
        print('Unknown "--act" passed')
