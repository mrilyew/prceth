from executables.extractors.Base.BaseIterableExtended import BaseIterableExtended
from representations.WebServices_Vk import BaseVk
from declarable.ArgumentsTypes import JsonArgument, IntArgument, LimitedArgument
from submodules.Uncanon.WebServices.VkApi import VkApi
from resources.Consts import consts

class VkFave(BaseIterableExtended):
    category = 'WebServices_Vk'

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

            from representations.WebServices_Vk.VkIdentity import VkIdentity
            from representations.WebServices_Vk.VkPost import VkPost
            from representations.WebServices_Vk.VkVideo import VkVideo
            from representations.WebServices_Vk.VkArticle import VkArticle
            from representations.WebServices_Vk.VkLink import VkLink

            match(i.get('section')):
                case 'users' | 'groups' | 'hints':
                    self.params['_method'] = 'fave.getPages'
                    self.params['_execute'] = {
                        'type': i.get('section')
                    }
                    self.params['_class'] = VkIdentity
                case 'post' | 'video' | 'article' | 'link':
                    self.params['_method'] = 'fave.get'
                    self.params['_execute'] = {
                        "item_type": i.get("section"),
                        "extended": 1,
                    }

                    match(i.get('section')):
                        case 'post':
                            self.params['_class'] = VkPost
                        case 'video':
                            self.params['_class'] = VkVideo
                        case 'article':
                            self.params['_class'] = VkArticle
                        case 'link':
                            self.params['_class'] = VkLink

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
