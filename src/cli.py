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
    
    # Collections get actions

    case 'collections.getItems':
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
