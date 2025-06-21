from app.App import logger
import asyncio

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
                await method_name(item, __list)
            except Exception as _exc:
                logger.logException(_exc, section=logger.SECTION_EXECUTABLES)

        return __list

    def self_insert(self, json_data: dict)->dict:
        '''
        You can append 'extractor' or 'representation' key there
        '''

        return json_data
