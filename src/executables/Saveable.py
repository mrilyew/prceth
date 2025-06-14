from db.ContentUnit import ContentUnit
from db.ContentUnit import StorageUnit
import asyncio

class Saveable:
    def contentUnit(self, json_data):
        return ContentUnit.fromJson(self.self_insert(json_data))

    def storageUnit(self, json_data = {}):
        return StorageUnit()

    async def gatherList(self, items, method_name):
        __list = []
        __tasks = []
        for item in items:
            __task = asyncio.create_task(method_name(item, __list))
            __tasks.append(__task)

        await asyncio.gather(*__tasks, return_exceptions=False)

        return __list
