from plugins.BasePlugins import BaseService
from resources.globals import time

class sample(BaseService):
    name = 'sample'
    interval = 10
    format = ''

    def action(self):
        print('ping | time: ' + str(time.time()))
