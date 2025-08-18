from executables.extractors.BaseIterableExtended import BaseIterableExtended
from declarable.ArgumentsTypes import IntArgument, CsvArgument
from executables.representations.WebServices_Vk.Message import Message
from submodules.Trivia.WebServices.VkApi import VkApi

class Messages(BaseIterableExtended):
    @classmethod
    def declare(cls):
        params = {}
        params.update(Message.declareVk())
        params["peer_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["attachments_info"] = CsvArgument({
            "default": "*",
        })
        params["attachments_file"] = CsvArgument({
            "default": "photo",
        })

        return params

    class ExecuteStrategy(BaseIterableExtended.ExecuteStrategy):
        def __init__(self, i = {}):
            super().__init__(i)

            self.params['vkapi'] = VkApi(token=i.get("access_token"),endpoint=i.get("api_url"))
            self.params['_method'] = 'messages.getHistory'
            self.params['_execute'] = {
                'peer_id': i.get('peer_id'),
                'extended': 1,
            }

        async def _get_count(self):
            _dct = self.params.get('_execute').copy()
            _dct.update({
                'count': 1
            })

            cnt = await self.params.get('vkapi').call(self.params.get('_method'), _dct)

            return cnt.get('count')

        async def iterate(self, time):
            offset = self.params.get('per_page') * time

            _dct = self.params.get('_execute').copy()
            _dct.update({
                'count': self.params.get('per_page'),
                'offset': offset,
            })

            _items = await self.params.get('vkapi').call(self.params.get('_method'), _dct)

            return await Message.extract({
                'object': _items
            })
