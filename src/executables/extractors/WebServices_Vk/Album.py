from declarable.ArgumentsTypes import IntArgument, BooleanArgument
from executables.extractors.BaseIterableExtended import BaseIterableExtended
from executables.representations.WebServices_Vk.Album import Album as VkAlbumRepresentation
from submodules.Trivia.WebServices.VkApi import VkApi

class Album(BaseIterableExtended):
    @classmethod
    def declare(cls):
        params = {}
        params.update(VkAlbumRepresentation.declareVk())
        params["owner_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["album_id"] = IntArgument({
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
            self.params['album_id'] = i.get('album_id')

        async def _get_collection(self):
            return await VkAlbumRepresentation.extract({
                'ids': f"{self.params.get('owner_id')}_{self.params.get('album_id')}"
            })

        async def _get_count(self):
            _ln = len(self.params.get('collections'))

            assert _ln == 1, 'wrong count of albums'
            assert self.params.get('collections')[0] != None, 'album not found'

            self.params['album_entity'] = VkAlbumRepresentation().hydrate(self.params.get('collections')[0])

            return self.params.get('collections')[0].json_content.get('size')

        async def iterate(self, time):
            offset = self.params.get('per_page') * time

            _items = await self.params.get('album_entity').getPhotos(self.params.get('vkapi'), count=self.params.get('per_page'), offset=offset, download=self.params.get('download'))

            return _items
