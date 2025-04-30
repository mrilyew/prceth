from executables.extractors.Base.Base import BaseExtractor
from resources.Globals import asyncio, logger
from db.File import File

# ЖИРИНОВСКИЙ СЧИТАЕТ, 1234
class IterableBase(BaseExtractor):
    name = 'IterableBase'
    category = 'base'

    def declare():
        params = {}
        params["start"] = {
            "type": "int",
            "desc_key": "-",
            "default": 1,
            "assertion": {
                "assert_not_null": True,
            }
        }
        params["end"] = {
            "type": "int",
            "desc_key": "-",
            "default": 100,
            "assertion": {
                "assert_not_null": True,
            }
        }
        params["timeout"] = {
            "type": "float",
            "desc_key": "-",
            "default": 1,
            "assertion": {
                "assert_not_null": True,
            }
        }

        return params

    def _getCollectionName(self):
        return f"Iterable {self.passed_params.get("start")}-{self.passed_params.get("end")}"

    async def run(self, args):
        self.entity_list = []

        for i in range(self.passed_params.get("start"), self.passed_params.get("end")):
            try:
                await self._iterableAction(i)
            except Exception as ____e:
                logger.logException(____e, "IterableBase", silent=False)

            await asyncio.sleep(self.passed_params.get("timeout"))

        return {
            "entities": self.entity_list,
            "collection": {
                "suggested_name": self._getCollectionName(),
            },
        }

    async def _iterableAction(self, i):
        pass
