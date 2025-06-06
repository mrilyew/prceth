from executables.extractors.Base.BaseCollectionable import BaseCollectionable
from app.App import logger
import asyncio

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
            "suggested_name": f"Iterable {args.get("start")}-{args.get("end")}",
        }

    async def run(self, args):
        self.ContentUnit_list = []

        for i in range(args.get("start"), args.get("end")):
            try:
                await self._iterableAction(i)
            except Exception as ____e:
                logger.logException(____e, "IterableBase", silent=False)

            await asyncio.sleep(args.get("timeout"))

        return {
            "entities": self.ContentUnit_list,
        }

    async def _iterableAction(self, i):
        pass
