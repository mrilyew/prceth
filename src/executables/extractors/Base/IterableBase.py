from app.App import logger
from declarable.ArgumentsTypes import IntArgument, FloatArgument
import asyncio

class IterableBase():
    name = 'IterableBase'
    category = 'base'

    def declare():
        params = {}
        params["start"] = IntArgument({
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        })
        params["end"] = IntArgument({
            "default": 100,
            "assertion": {
                "not_null": True,
            }
        })
        params["timeout"] = FloatArgument({
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def run(self, i):
        self.cu_list = []

        for i in range(i.get("start"), i.get("end")):
            try:
                await self._iterableAction(i)
            except Exception as ____e:
                logger.logException(____e, "IterableBase", silent=False)

            await asyncio.sleep(i.get("timeout"))

        return self.cu_list

    async def _iterableAction(self, i):
        pass
