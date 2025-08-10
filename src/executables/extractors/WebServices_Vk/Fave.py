from executables.extractors.BaseIterableExtended import BaseIterableExtended
from executables.representations.WebServices_Vk import BaseVk
from declarable.ArgumentsTypes import JsonArgument, IntArgument, LimitedArgument
from submodules.Trivia.WebServices.VkApi import VkApi
from resources.Consts import consts

class Fave(BaseIterableExtended):
    @classmethod
    def declare(cls):
        params = {}
        params.update(BaseVk.declareVk())
        params["section"] = LimitedArgument({
            'values': ['users', 'groups', 'hints', 'post', 'video', 'article', 'link'],
            'assertion': {
                'not_null': True,
            }
        })
        params["tag_id"] = IntArgument({})
        params["appends"] = JsonArgument({})

        return params

    class ExecuteStrategy(BaseIterableExtended.ExecuteStrategy):
        def __init__(self, i = {}):
            super().__init__(i)

            self.params['vkapi'] = VkApi(token=i.get("api_token"),endpoint=i.get("api_url"))
            self.params['appends'] = i.get('appends')
            self.params['_class'] = None
            self.params['_method'] = ''
            self.params['_execute'] = {}

            from executables.representations.WebServices_Vk.Identity import Identity
            from executables.representations.WebServices_Vk.Post import Post
            from executables.representations.WebServices_Vk.Video import Video
            from executables.representations.WebServices_Vk.Article import Article
            from executables.representations.WebServices_Vk.Link import Link

            match(i.get('section')):
                case 'users' | 'groups' | 'hints':
                    self.params['_method'] = 'fave.getPages'
                    self.params['_execute'] = {
                        'type': i.get('section')
                    }
                    self.params['_class'] = Identity
                case 'post' | 'video' | 'article' | 'link':
                    self.params['_method'] = 'fave.get'
                    self.params['_execute'] = {
                        "item_type": i.get("section"),
                        "extended": 1,
                    }

                    match(i.get('section')):
                        case 'post':
                            self.params['_class'] = Post
                        case 'video':
                            self.params['_class'] = Video
                        case 'article':
                            self.params['_class'] = Article
                        case 'link':
                            self.params['_class'] = Link

            BaseVk.define()
            self.params.get('_execute')['fields'] = ",".join(consts.get("vk.min_group_fields") + consts.get("vk.min_user_fields"))

            if 'tag_id' in i:
                self.params.get('_execute')['tag_id'] = i.get('tag_id')

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
            resp = {
                'items': [],
                'profiles': _items.get('profiles'),
                'groups': _items.get('groups')
            }

            for item in _items.get('items'):
                resp.get('items').append(item.get(item.get('type')))

            _t = {
                'object': resp,
            }

            if 'appends' in self.params:
                _t.update(self.params.get('appends'))

            obj = await self.params.get('_class').extract(_t)

            return obj
