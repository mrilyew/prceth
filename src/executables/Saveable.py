from app.App import logger
import asyncio
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit

class Saveable:
    async def gatherList(self, items, method_name, is_gather = True):
        __list = []
        __tasks = []

        if is_gather == True:
            for item in items:
                __task = asyncio.create_task(method_name(item, __list))
                __tasks.append(__task)

            await asyncio.gather(*__tasks, return_exceptions=False)
        else:
            try:
                for item in items:
                    await method_name(item, __list)
            except Exception as _exc:
                logger.logException(_exc, section=logger.SECTION_EXECUTABLES)

        return __list

    # signed

    def ContentUnit(self):
        out = ContentUnit()
        self.self_insert(out)

        return out

    def StorageUnit(self):
        out = StorageUnit()

        return out

    def self_insert(self, item):
        '''
        You can append needed keys here
        '''

        return item
