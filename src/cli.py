from core.api import api
from resources.globals import utils
from db.collection import Collection
from resources.prefetch import prefetch__db

prefetch__db()

args = utils.parse_args()
match args.get('act'):
    case None:
        print('"--act" not passed.')
    
    # Config actions

    case "config.get":
        if 'param' in args:
            print(api.getOption(args['param']))
        else:
            print('\'--param\' not passed.')
    case "config.set":
        if 'param' in args and 'value' in args:
            api.setOption(args.get('param'), args['value'])
        else:
            print('\'--param\' and \'--value\' are not passed.')
    case "config.reset":
        api.resetOptions()
    case "config.all":
        options = api.getAllOptions()
        for option in options:
            print("|" + option + "|" + options[option] + "|")
    case 'logger.log':
        from submodules.logger import logger
        logger.log(args.get('section'), args.get('name'), args.get('message'))
    
    # Collections write actions
    
    case "collections.create":
        final_params = dict()

        if 'name' not in args:
            print('Error: "--name" not passed')
            exit(-1)

        final_params["name"] = args.get("name")
        final_params["description"] = args.get("description")

        if args.get('frontend_type') != None:
            final_params['frontend_type'] = args.get('frontend_type')
        
        if args.get('icon_hash') != None:
            final_params['icon_hash'] = args.get('icon_hash')
        
        if args.get('add_after') != None:
            final_params['hidden'] = 1
            to_add = Collection.get(args.get('add_after'))
            if to_add == None:
                print('Invalid collection')
                exit(-1)
            
            final_params['to_add'] = to_add
        
        api.createCollection(final_params)
    case 'collections.edit':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)
        
        if 'name' not in args:
            print('Error: "--name" not passed')
            exit(-1)

        final_params = dict()
        final_params["collection_id"] = args.get('id')
        if 'name' in args:
            final_params['name'] = args.get('name')
        if 'description' in args:
            final_params['description'] = args.get('description')      
        if 'frontend_type' in args:
            final_params['frontend_type'] = args.get('frontend_type')                      
        if 'icon_hash' in args:
            final_params['icon_hash'] = args.get('icon_hash')

        api.editCollection(final_params)
    case 'collections.delete':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)

        final_params = dict()
        final_params["collection_id"] = args.get('id')

        api.deleteCollection(final_params)
    case 'collections.switch':
        if 'id1' not in args and 'id2' not in args:
            print('Error: "--id1" and "--id2" are not passed')
            exit(-1)

        final_params = dict()
        final_params["id1"] = args.get('id1')
        final_params["id2"] = args.get('id2')
        api.switchCollections(final_params)
    case 'collections.appendItem':
        if 'collection_id' not in args and 'entity_id' not in args:
            print('Error: "--collection_id" and "--entity_id" are not passed')
            exit(-1)

        final_params = dict()
        final_params["collection_id"] = args.get('collection_id')
        final_params["entity_id"] = args.get('entity_id')

        api.addItemToCollection(final_params)
    case 'collections.removeItem':
        if 'collection_id' not in args and 'entity_id' not in args:
            print('Error: "--collection_id" and "--entity_id" are not passed')
            exit(-1)

        final_params = dict()
        final_params["collection_id"] = args.get('collection_id')
        final_params["entity_id"] = args.get('entity_id')

        api.removeItemFromCollection(final_params)

    # Collections get actions

    case 'collections.get':
        final_params = dict()
        final_params["query"] = args.get("query")
        final_params["offset"] = args.get("offset")
        final_params["count"] = args.get("count")

        items, count = api.getItems(final_params)

        print("Total {0} items".format(count))
        for item in items:
            print(str(item.getApiStructure()) + "\n")
    case 'collections.getItems':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)
        
        final_params = dict()
        final_params["collection_id"] = args.get('id')
        final_params["query"] = args.get("query")
        final_params["offset"] = args.get("offset")
        final_params["count"] = args.get("count")
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if args.get("search_by_" + column) != None:
                columns_search.append(column)

        final_params["columns_search"] = columns_search
        items = api.getItemsInCollection(final_params)
        for item in items:
            print(str(item.getApiStructure()) + "\n")
    case 'collections.getItemsCount':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)
        
        final_params = dict()
        final_params["collection_id"] = args.get('id')
        final_params["query"] = args.get("query")
        final_params["offset"] = args.get("offset")
        final_params["limit"] = args.get("count")
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if args.get("search_by_" + column) != None:
                columns_search.append(column)

        final_params["columns_search"] = columns_search
        print(api.getItemsCountInCollection(final_params))
    case 'collections.getById':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)

        final_params = dict()
        final_params["collection_id"] = args.get('id')
        
        collection = api.getCollectionById(final_params)
        print(collection.getApiStructure())

    # Entities write actions

    case 'entities.remove':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)

        final_params = dict()
        final_params["entity_id"] = args.get('id')
        final_params["delete_file"] = args.get('delete_file') == "1"

        act = api.removeEntity(final_params)
    case 'entities.edit':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)

        final_params = dict()
        final_params["entity_id"] = args.get("id")
        final_params["display_name"] = args.get("name")
        final_params["description"] = args.get("description")

        act = api.editEntity(final_params)
    case 'entities.new':
        if 'extractor' not in args:
            print('"--extractor" not passed')
            exit()

        act = api.uploadEntity(args)
        if type(act) == str:
            print(act)
        else:
            print(act.getApiStructure())
    
    # Entities get actions

    case 'entities.getById':
        if 'id' not in args:
            print('Error: "--id" not passed')
            exit(-1)

        final_params = dict()
        final_params["entity_id"] = args.get("id")
        entity = api.getEntityById(final_params)

        print(entity.getApiStructure())
    case 'entities.get':
        final_params = dict()
        final_params["query"] = args.get("query")
        final_params["offset"] = args.get("offset", 0)
        final_params["count"] = args.get("count", 10)
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if args.get("search_by_" + column) != None:
                columns_search.append(column)

        final_params["columns_search"] = columns_search
        items, count = api.getGlobalEntities(final_params)

        print("Total {0} items\n".format(count))
        for item in items:
            print(str(item.getApiStructure()) + "\n")

    # Extractors

    case 'extractors.get':
        final_params = dict()
        final_params["show_hidden"] = args.get("show_hidden", None) != None

        items = api.getExtractors(final_params)
        for item in items:
            print(str(item.describe()) + "\n")
    case 'acts.get':
        final_params = dict()
        final_params["show_hidden"] = args.get("show_hidden", None) != None
        final_params["search_type"] = args.get("search_type", "all")

        items = api.getActs(final_params)
        for item in items:
            print(str(item.describe()) + "\n")
    case 'acts.run':
        if 'act_name' not in args:
            print('"--act_name" not passed')
            exit()

        print(api.runAct(args))
    case 'services.get':
        final_params = dict()
        final_params["show_hidden"] = args.get("show_hidden", None) != None
        final_params["search_type"] = args.get("search_type", "all")

        items = api.getServices(final_params)
        for item in items:
            print(str(item.describe()) + "\n")
    case 'services.run':
        if 'service_name' not in args:
            print('"--service_name" not passed')
            exit()

        print("Started service")
        api.runService(args)
    case _:
        print('Unknown "--act" passed')
        exit(-14)
