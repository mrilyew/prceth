from app.App import logger
import asyncio

class IterableBase():
    name = 'IterableBase'
    category = 'base'

    def declare():
        params = {}
        params["start"] = {
            "type": "int",
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        }
        params["end"] = {
            "type": "int",
            "default": 100,
            "assertion": {
                "not_null": True,
            }
        }
        params["timeout"] = {
            "type": "float",
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        }

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
