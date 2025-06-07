from utils.MainUtils import dump_json
from app.App import logger
from executables.Executable import Executable
import asyncio, time

class BaseService(Executable):
    name = 'base'
    config = {}
    interval = 10
    i = 0
    service_object = None

    def __init__(self):
        self.is_stopped = False

    async def iteration(self, i):
        logger.log(message=f"Making run №{self.i + 1}", kind="message", section="Services")
        self.i = self.i+1

        return await self.execute(i)

    def stop(self):
        self.is_stopped = True

    def execute(self, args = {}):
        pass

    def terminate(self):
        exit(-1)
