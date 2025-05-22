from resources.Globals import time, asyncio, logger
from executables.Executable import Executable

class BaseService(Executable):
    name = 'base'
    config = {}
    interval = 10
    i = 0

    def __init__(self):
        self.is_stopped = False

    def setConfig(self, conf):
        self.config = conf

    async def start(self):
        await self.action_wrapper()

    async def action_wrapper(self):
        while not self.is_stopped:
            logger.log(message=f"Making call №{self.i}",name="message",section="Services")

            try:
                print(await self.execute(self.passed_params))
            except Exception as e:
                logger.logException(input_exception=e,section="Services",silent=False)

            logger.log(message=f"Sleeping for {self.interval}",name="message",section="Services")

            await asyncio.sleep(self.interval)

            self.i = self.i+1

    def stop(self):
        self.is_stopped = True

    def execute(self, args = {}):
        pass
