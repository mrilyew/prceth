from declarable.ArgumentsTypes import IntArgument, BooleanArgument
from executables.extractors.Base.BaseIterableExtended import BaseIterableExtended
from representations.WebServices_Vk.VkPhoto import VkPhoto
from submodules.Uncanon.WebServices.VkApi import VkApi

class VkAllPhotos(BaseIterableExtended):
    category = 'WebServices_Vk'

    @classmethod
    def declare(cls):
        params = {}
        params.update(VkPhoto.declareVk())
        params["owner_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["download"] = BooleanArgument({
            "default": True
        })

        return params

    class ExecuteStrategy(BaseIterableExtended.ExecuteStrategy):
        def __init__(self, i = {}):
            super().__init__(i)

            self.params['vkapi'] = VkApi(token=i.get("api_token"),endpoint=i.get("api_url"))
            self.params['owner_id'] = i.get('owner_id')

        async def _get_count(self):
            return await VkPhoto.countByUser(self.params.get('vkapi'), self.params.get('owner_id'))

        async def iterate(self, time):
            offset = self.params.get('per_page') * time

            _items = await VkPhoto.byUser(self.params.get('vkapi'), owner_id=self.params.get('owner_id'), count=self.params.get('per_page'), offset=offset, download=self.params.get('download'))

            return _items
