from plugins.upload_plugins.vk.vk import base_vk
from resources.globals import urlencode, requests, json, utils, consts, settings

class wall(base_vk):
    name = 'vk.wall'
    works = 'all'
    category = 'vk'
    short_name = 'wall'

    def run(self, args=None):
        # Args
        self.check_args(args=args)

        print('Dummy')
