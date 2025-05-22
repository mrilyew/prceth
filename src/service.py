from resources.Globals import utils, asyncio, loop, json, ServicesRepository, logger, time
from resources.DbPrefetch import prefetch__db
from db.Service import Service

prefetch__db()

args = utils.parse_args()

async def runService():
    assert "i" in args, "i not passed"

    __service_id = args.get("i")
    __service_settings = Service.get(__service_id)

    assert __service_settings != None, "service preset not found"
    
    __service_name = __service_settings.service_name
    __service_res = ServicesRepository().getByName(service_name=__service_name)
    __data = utils.parse_json(__service_settings.data)

    OUT_SERV = __service_res()
    OUT_SERV.setConfig(__data)
    OUT_SERV.interval = __service_settings.interval
    OUT_SERV.setArgs(args)

    try:
        await OUT_SERV.start()
    except Exception as e:
        logger.logException(e)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        OUT_SERV.stop()

loop.run_until_complete(runService())
