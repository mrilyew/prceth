from declarable.ArgumentsTypes import IntArgument, StringArgument, CsvArgument, BooleanArgument
from executables.extractors.BaseIterableExtended import BaseIterableExtended
from executables.representations.WebServices_Vk.Post import Post
from submodules.Trivia.WebServices.VkApi import VkApi

class Wall(BaseIterableExtended):
    @classmethod
    def declare(cls):
        params = {}
        params.update(Post.declareVk())
        params["owner_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["filter"] = StringArgument({
            "default": 'all',
        })
        params["attachments_info"] = CsvArgument({
            "default": "*",
        })
        params["attachments_file"] = CsvArgument({
            "default": "photo",
        })
        params["download_reposts"] = BooleanArgument({
            'default': True,
        })

        return params

    class ExecuteStrategy(BaseIterableExtended.ExecuteStrategy):
        def __init__(self, i = {}):
            super().__init__(i)

            self.params['vkapi'] = VkApi(token=i.get("access_token"),endpoint=i.get("api_url"))
            self.params['owner_id'] = i.get('owner_id')
            self.params['filter'] = i.get('filter')
            self.params['attachments_info'] = i.get('attachments_info')
            self.params['attachments_file'] = i.get('attachments_file')
            self.params['download_reposts'] = i.get('download_reposts')

        async def _get_count(self):
            return await Post.wallCount(self.params.get('vkapi'), self.params.get('owner_id'), self.params.get('filter'))

        async def iterate(self, time):
            offset = self.params.get('per_page') * time

            response = await Post.wall(self.params.get('vkapi'), owner_id=self.params.get('owner_id'), filter=self.params.get('filter'), count=self.params.get('per_page'), offset=offset)
            _items = await Post.extract({
                'object': response,
                'attachments_info': self.params.get('attachments_info'),
                'attachments_file': self.params.get('attachments_file'),
                'download_reposts': self.params.get('download_reposts'),
            })

            return _items
