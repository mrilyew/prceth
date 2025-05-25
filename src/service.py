from resources.Globals import utils, asyncio, loop, json, ServicesRepository, logger, time
from resources.DbPrefetch import prefetch__db
from db.Service import Service

prefetch__db()

args = utils.parse_args()

async def runService():
    assert "i" in args, "i not passed"

    __service_id = args.get("i")
    __service_settings = Service.get(__service_id)
    __input_interval = args.get("interval")

    assert __service_settings != None, "service preset not found"
    
    __service_name = __service_settings.service_name
    __service_res = ServicesRepository().getByName(service_name=__service_name)
    __data = utils.parse_json(__service_settings.data)

    OUT_SERV = __service_res()
    OUT_SERV.setConfig(__data)
    OUT_SERV.service_object = __service_settings
    OUT_SERV.setArgs(args)

    interval = 0

    if __input_interval == None:
        interval = int(__service_settings.interval)
    else:
        interval = int(__input_interval)

    try:
        while True:
            await OUT_SERV.run()
    
            logger.log(message=f"Sleeping for {interval}s",name="message",section="Services")

            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        OUT_SERV.stop()

loop.run_until_complete(runService())
