from plugins.BasePlugins import BaseUploadPlugin
from core.settings import settings
from resources.consts import consts

class base_vk(BaseUploadPlugin):
    name = 'vk.base'
    short_name = 'base'
    format = '%'
    works = 'all'
    category = 'vk'

    def check_args(self, args):
        self.id = args.get('id')
        if self.id == None:
            raise AttributeError("Id was not passed")

        if self.id.find(self.short_name) != -1:
            self.id = self.id.replace(self.short_name, '')

        self.vk_token = args.get('vk_token')
        if self.vk_token == None:
            self.vk_token = settings.get('vk.access_token')

        if self.vk_token == None:
            raise AttributeError("Token was not passed")

        self.user_agent = args.get('user_agent')
        if self.user_agent == None:
            self.user_agent = consts.get('vk.cool_useragent')
        
        self.vk_url = args.get('vk_url')
        self.vk_web_url = args.get('vk_web_url')
        if self.vk_url == None:
            self.vk_url = 'https://api.vk.com/method/'

        if self.vk_web_url == None:
            self.vk_web_url = 'https://vk.com/'
