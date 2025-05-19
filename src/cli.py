from core.Api import api
from resources.Globals import utils, asyncio, loop, json
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

        case 'entities.new':
            act = await api.uploadEntity(args)
            if type(act) == str:
                print(act)
            else:
                #print(act.getApiStructure())
                pass

        # Extractors

        case 'extractors.get':
            items = api.getExtractors(args)
            for item in items:
                print(json.dumps(item.describe(), indent=4, ensure_ascii=False))
        case 'acts.get':
            items = api.getActs(args)
            for item in items:
                print(str(item.describe()))
        case 'acts.run':
            print(await api.runAct(args))
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

loop.run_until_complete(__cliMain())
