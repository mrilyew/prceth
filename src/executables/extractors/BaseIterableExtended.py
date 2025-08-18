from executables.extractors import BaseExtractor
from executables.extractors.BaseTimeoutable import BaseTimeoutable
from declarable.ArgumentsTypes import IntArgument
from resources.Exceptions import AbstractClassException
from app.App import logger
import math, asyncio

class BaseIterableExtended(BaseTimeoutable, BaseExtractor):
    class ExecuteStrategy():
        params = {}

        def __init__(self, i = {}):
            self.params['downloaded_count'] = 0
            self.params['limit_count'] = i.get('limit')
            self.params['first_iteration'] = i.get('first_iteration')
            self.params['per_page'] = i.get('per_page')
            self.params['preset_total_count'] = i.get('preset_total_count')
            self.params['collections'] = []

        async def set_count(self):
            self.params['total_count'] = await self._get_count()
            if self.params.get('preset_total_count') != None:
                self.params['total_count'] = self.params.get('preset_total_count')

            self.params['call_times'] = math.ceil(self.params.get('total_count') / self.params.get('per_page'))

        async def _get_count(self):
            raise AbstractClassException()

        async def iterate(self, time):
            raise AbstractClassException()
 
    @classmethod
    def declare(cls):
        params = {}
        params["first_iteration"] = IntArgument({
            "default": 0
        })
        params["max_iteration"] = IntArgument({
            "default": 0
        })
        params["preset_total_count"] = IntArgument({
            "default": None,
        })
        params["limit"] = IntArgument({
            "default": 0,
        })
        params["per_page"] = IntArgument({
            "default": 100
        })

        return params

    async def execute(self, i = {}):
        max_iteration = i.get('max_iteration')
        _strategy = self.__class__.ExecuteStrategy(i)

        if getattr(_strategy, '_get_collection', None) != None:
            cols = await _strategy._get_collection()
            _strategy.params['collections'] = cols

            for col in cols:
                self.link_after_add(col)

        await _strategy.set_count()

        logger.log(message=f"Total {_strategy.params.get('total_count')} items; will be {_strategy.params.get('call_times')} calls",section="Iterable!Extended", kind=logger.KIND_MESSAGE)

        for time in range(_strategy.params.get('first_iteration'), _strategy.params.get('call_times')):
            if max_iteration > 0 and time > max_iteration:
                return
            
            if _strategy.params.get('limit_count') > 0 and (_strategy.params.get('downloaded_count') > _strategy.params.get('limit_count')):
                return

            logger.log(message=f"{time + 1}/{_strategy.params.get('call_times')} time of items recieving",section="Iterable!Extended",kind=logger.KIND_MESSAGE)

            _items = await _strategy.iterate(time)
            for _item in _items:
                _strategy.params['downloaded_count'] += 1

                if _strategy.params.get('limit_count') > 0:
                    if _strategy.params.get('downloaded_count') > _strategy.params.get('limit_count'):
                        continue

                self.linked_dict.append(_item)

            if i.get("timeout") != 0:
                await asyncio.sleep(i.get("timeout"))
