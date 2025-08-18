from declarable.ArgumentsTypes import IntArgument, CsvArgument, LimitedArgument
from executables.extractors.BaseIterableExtended import BaseIterableExtended
from executables.representations.WebServices_Vk.Comment import Comment
from submodules.Trivia.WebServices.VkApi import VkApi

class Comments(BaseIterableExtended):
    @classmethod
    def declare(cls):
        params = {}
        params.update(Comment.declareVk())
        params["owner_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["target_id"] = IntArgument({
            'assertion': {
                'not_null': True,
            }
        })
        params["sort"] = LimitedArgument({
            "default": 'asc',
            "values": ["asc", "desc"],
        })
        params["comment_id"] = IntArgument({})
        params["thread_items_count"] = IntArgument({
            'default': 100
        })
        params["target"] = LimitedArgument({
            "default": "post",
            "values": ["board", "post", "video", "photo", "photo_all", "note"]
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
            self.params['attachments_info'] = i.get('attachments_info')
            self.params['attachments_file'] = i.get('attachments_file')
            self.params['_method'] = ''
            self.params['_execute'] = {
                "need_likes": 1, 
                "sort": self.params.get("sort"),
                "extended": 1,
                "thread_items_count": self.params.get("thread_items_count", 10),
            }

            match(i.get('target')):
                case 'post':
                    self.params.get('_execute')['owner_id'] = i.get('owner_id')
                    self.params.get('_execute')['post_id'] = i.get('target_id')
                    self.params['_method'] = 'wall.getComments'
                    if 'comment_id' in i:
                        self.params['comment_id'] = i.get('comment_id')
                case 'board':
                    self.params.get('_execute')['group_id'] = abs(i.get('owner_id'))
                    self.params.get('_execute')['topic_id'] = i.get('target_id')
                    self.params['_method'] = 'board.getComments'
                case 'note':
                    self.params.get('_execute')['owner_id'] = i.get('owner_id')
                    self.params.get('_execute')['note_id'] = i.get('target_id')
                    self.params['_method'] = 'notes.getComments'
                case 'photo_all':
                    self.params.get('_execute')['owner_id'] = i.get('owner_id')
                    self.params.get('_execute')['album_id'] = i.get('target_id')
                    self.params['_method'] = 'photos.getAllComments'
                case 'photo':
                    self.params.get('_execute')['owner_id'] = i.get('owner_id')
                    self.params.get('_execute')['photo_id'] = i.get('target_id')
                    self.params['_method'] = 'photos.getComments'
                case 'video':
                    self.params.get('_execute')['owner_id'] = i.get('owner_id')
                    self.params.get('_execute')['video_id'] = i.get('target_id')
                    self.params['_method'] = 'video.getComments'

        async def _get_count(self):
            _dct = self.params.get('_execute').copy()
            _dct.update({
                'count': 1
            })

            _cnt = await self.params.get('vkapi').call(self.params.get('_method'), _dct)

            return _cnt.get('count')

        async def iterate(self, time):
            offset = self.params.get('per_page') * time
            _dct = self.params.get('_execute').copy()
            _dct.update({
                'count': self.params.get('per_page'),
                'offset': offset,
            })

            _items = await self.params.get('vkapi').call(self.params.get('_method'), _dct)
            return await Comment.extract({
                'object': _items
            })
