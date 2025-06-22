from app.App import logger
from executables.extractors.BaseTimeoutable import BaseTimeoutable
from declarable.ArgumentsTypes import IntArgument
import asyncio

class BaseIterable(BaseTimeoutable):
    category = 'base'

    @classmethod
    def declare(cls):
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

        return params

    async def execute(self, i):
        for iterator in range(i.get("start"), i.get("end")):
            try:
                await self._iterableAction(i, iterator)
            except Exception as ____e:
                logger.logException(____e, "Iterable", silent=False)

            await asyncio.sleep(i.get("timeout"))

    async def _iterableAction(self, i):
        pass
