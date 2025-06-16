from executables.extractors.Base.BaseTimeoutable import BaseTimeoutable
from executables.extractors.Base.Base import BaseExtractor
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

        async def set_count(self):
            self.params['total_count'] = await self._get_count()
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
        params["limit"] = IntArgument({
            "default": 0,
        })
        params["per_page"] = IntArgument({
            "default": 100
        })

        return params

    async def execute(self, i = {}):
        _strategy = self.__class__.ExecuteStrategy(i)
        await _strategy.set_count()

        logger.log(message=f"Total {_strategy.params.get('total_count')} items; will be {_strategy.params.get('call_times')} calls",section="Iterable!Extended",kind="message")

        for time in range(_strategy.params.get('first_iteration'), _strategy.params.get('call_times')):
            if _strategy.params.get('downloaded_count') > 0 and (_strategy.params.get('downloaded_count') > _strategy.params.get('limit_count')):
                return []

            logger.log(message=f"{time + 1}/{_strategy.params.get('call_times')} time of items recieving",section="Iterable!Extended",kind="message")

            _items = await _strategy.iterate(time)
            for _item in _items:
                _strategy.params['downloaded_count'] += 1

                if _strategy.params.get('limit_count') > 0:
                    if _strategy.params.get('downloaded_count') > _strategy.params.get('limit_count'):
                        continue

                self.linked_dict.append(_item)

            if i.get("timeout") != 0:
                await asyncio.sleep(i.get("timeout"))
