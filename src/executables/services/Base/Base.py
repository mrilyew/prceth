from utils.MainUtils import parse_json, dump_json
from app.App import logger
from resources.Exceptions import EndOfCycleException
from declarable.ArgsValidator import ArgsValidator
from executables.Executable import Executable
import asyncio, time

class BaseService(Executable):
    name = 'base'
    config = {}
    interval = 10
    current_iterator = 0
    max_iterations = 0
    service_object = None

    def __init__(self):
        self.is_stopped = False

    async def iteration(self, i):
        self.current_iterator = self.current_iterator+1

        __end = '∞'
        if self.max_iterations > 0:
            if self.current_iterator > self.max_iterations:
                raise EndOfCycleException("Reached the end of cycle")

            __end = self.max_iterations

        logger.log(message=f"Making run {self.current_iterator}/{__end}", kind="message", section=logger.SECTION_SERVICES)

        return await self.execute(i)

    def stop(self):
        self.is_stopped = True

    def execute(self, args = {}):
        pass

    def terminate(self):
        exit(-1)

    def validate(self, args: dict)->dict:
        return ArgsValidator().validate(self.declare_recursive(), args, self.executable_cfg)
