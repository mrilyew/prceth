from app.App import app, logger
from db.ServiceInstance import ServiceInstance
from repositories.ServicesRepository import ServicesRepository
from utils.MainUtils import parse_json, dump_json
from resources.Exceptions import FatalError, EndOfCycleException
from datetime import datetime
import asyncio

async def runService():
    assert "i" in app.argv, "service_instance id (--i) not passed"

    __service_id = app.argv.get("i")
    __service_settings = ServiceInstance.get(__service_id)
    __input_interval = app.argv.get('interval')
    __max_iterations = int(app.argv.get('max_iterations', 0))

    assert __service_settings != None, "service preset not found"

    __service_name = __service_settings.service_name

    __service_res = ServicesRepository().getByName(__service_name)
    __data = parse_json(__service_settings.data)

    service_out = __service_res()
    service_out.max_iterations = __max_iterations
    service_out.config = service_out.validate(__data)
    service_out.service_object = __service_settings

    interval = 0

    if __input_interval == None:
        interval = int(__service_settings.interval)
    else:
        interval = int(__input_interval)

    logger.log(message=f"Started at {datetime.now()}", kind="message", section="Services")

    try:
        while True:
            await service_out.iteration(app.argv)

            logger.log(message=f"Sleeping for {interval}s", kind="message", section="Services")

            await asyncio.sleep(interval)
    except KeyboardInterrupt:
        service_out.stop()
    except FatalError as _e:
        service_out.stop()

        raise _e
    except EndOfCycleException:
        service_out.stop()

app.loop.run_until_complete(runService())
