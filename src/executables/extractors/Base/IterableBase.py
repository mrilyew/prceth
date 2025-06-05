from executables.extractors.Base.BaseCollectionable import BaseCollectionable
from resources.Globals import asyncio, logger

# ЖИРИНОВСКИЙ СЧИТАЕТ, 1234
class IterableBase(BaseCollectionable):
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

    def _collection(self):
        return {
            "suggested_name": f"Iterable {self.passed_params.get("start")}-{self.passed_params.get("end")}",
        }

    async def run(self, args):
        self.ContentUnit_list = []

        for i in range(self.passed_params.get("start"), self.passed_params.get("end")):
            try:
                await self._iterableAction(i)
            except Exception as ____e:
                logger.logException(____e, "IterableBase", silent=False)

            await asyncio.sleep(self.passed_params.get("timeout"))

        return {
            "entities": self.ContentUnit_list,
        }

    async def _iterableAction(self, i):
        pass
