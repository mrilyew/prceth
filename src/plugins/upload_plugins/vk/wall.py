from core.settings import settings
from resources.consts import consts
from core.utils import utils
from plugins.upload_plugins.vk.vk import base_vk
from urllib.parse import urlencode
import requests
import json

class wall(base_vk):
    name = 'vk.wall'
    works = 'all'
    category = 'vk'
    short_name = 'wall'

    def run(self, args=None):
        # Args
        self.check_args(args=args)

        print('Dummy')
