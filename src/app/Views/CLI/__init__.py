from app.App import app, logger
from resources.Consts import consts
from utils.MainUtils import dump_json, parse_json
from executables.acts.Executables.RunAct import RunAct
from db.Models.Instances.ServiceInstance import ServiceInstance
from repositories.ServicesRepository import ServicesRepository
from resources.Exceptions import FatalError, EndOfCycleException
from datetime import datetime
import asyncio

consts['context'] = 'cli'

class CLI:
    async def act(self):
        assert "i" in app.argv, "pass the name of act as --i"
        is_silent = 'silent' in app.argv

        act = RunAct()
        output = await act.safeExecute(app.argv)

        if is_silent == False:
            print(dump_json(output, indent=4))

    async def service(self):
        assert "i" in app.argv, "service_instance id (--i) not passed"

        __service_id = app.argv.get("i")
        __service_settings = ServiceInstance.get(__service_id)
        __input_interval = app.argv.get('interval')
        __max_iterations = int(app.argv.get('max_iterations', 0))
        join_argv = int(app.argv.get('__join_argv', 0)) == 1

        assert __service_settings != None, "service preset not found"

        __service_name = __service_settings.service_name

        __service_res = ServicesRepository().getByName(__service_name)
        __data = parse_json(__service_settings.data)

        if join_argv == True:
            __data.update(app.argv)

        service_out = __service_res()
        service_out.max_iterations = __max_iterations
        service_out.config = service_out.validate(__data)
        service_out.service_object = __service_settings

        interval = 0

        if __input_interval == None:
            interval = int(__service_settings.interval)
        else:
            interval = int(__input_interval)

        logger.log(message=f"Started service", kind=logger.KIND_MESSAGE, section=logger.SECTION_SERVICES)

        try:
            while True:
                await service_out.iteration(app.argv)

                logger.log(message=f"Sleeping for {interval}s", kind=logger.KIND_MESSAGE, section=logger.SECTION_SERVICES)

                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            service_out.stop()
        except FatalError as _e:
            service_out.stop()

            raise _e
        except EndOfCycleException:
            service_out.stop()

cli = CLI()
