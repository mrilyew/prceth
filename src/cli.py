from core.Api import api
from resources.Globals import utils, asyncio, loop, Path
from resources.DbPrefetch import prefetch__db

prefetch__db()

args = utils.parse_args()

async def __cliMain():
    match args.get('act'):
        case None:
            print('"--act" not passed.')
        
        # Config actions

        case "config.get":
            if 'key' in args:
                print(api.getOption(args['key']))
            else:
                print('\'--param\' not passed.')
        case "config.set":
            if 'param' in args and 'value' in args:
                api.setOption(args.get('param'), args.get('value'))
            else:
                print('\'--param\' and \'--value\' are not passed.')
        case "config.setNull":
            api.resetOptions()
        case "config.getAll":
            options = api.getAllOptions()
            for option in options:
                print(f"{option}: {options[option]}")
        #case 'logger.log':
            #from resources.Globals import logger
            #logger.log(args.get('section'), args.get('name'), args.get('message'))
        # TODO logger.get
        
        # Collections write actions
        
        case "collections.create" | "collections.new":
            api.createCollection(args)
        case 'collections.edit':
            api.editCollection(args)
        case 'collections.delete':
            api.deleteCollection(args)
        case 'collections.switch':
            api.switchCollections(args)
        case 'collections.appendItem':
            api.addItemToCollection(args)
        case 'collections.removeItem':
            api.removeItemFromCollection(args)

        # Collections get actions

        case 'collections.get':
            items, count = api.getAllCollections(args)

            print("Total {0} items".format(count))
            for item in items:
                print(str(item.getApiStructure()) + "\n")
        case 'collections.getItems':
            items = api.getItemsInCollection(args)
            for item in items:
                print(str(item.getApiStructure()) + "\n")
        case 'collections.getItemsCount':
            print(api.getItemsCountInCollection(args))
        case 'collections.getById':
            collection = api.getCollectionById(args)
            print(collection.getApiStructure())

        # Entities write actions

        case 'entities.remove':
            act = api.removeEntity(args)
        case 'entities.edit':
            act = api.editEntity(args)
        case 'entities.new':
            act = await api.uploadEntity(args)
            if type(act) == str:
                print(act)
            else:
                #print(act.getApiStructure())
                pass
        
        # Entities get actions

        case 'entities.getById':
            entities = api.getEntityById(args)

            for entity in entities:
                print(entity.getApiStructure())
        case 'entities.get':
            items, count = api.getGlobalEntities(args)

            print("Total {0} items\n".format(count))
            for item in items:
                print(str(item.getApiStructure()))

        # Extractors

        case 'extractors.get':
            items = api.getExtractors(args)
            for item in items:
                print(str(item.describe()))
        case 'acts.get':
            items = api.getActs(args)
            for item in items:
                print(str(item.describe()))
        case 'acts.run':
            print(api.runAct(args))
        case 'services.get':
            items = api.getServices(args)
            for item in items:
                print(str(item.describe()))
        case 'services.run':
            print("Started service")
            api.runService(args)
        case _:
            print('Unknown "--act" passed')
            exit(-14)

try:
    loop.run_until_complete(__cliMain())
except KeyboardInterrupt:
    asyncio.sleep(10)
