import time
from plugins.BasePlugins import BaseService

class SampleService(BaseService):
    name = 'SampleService'
    interval = 10
    format = ''

    def action(self):
        print('ping | time: ' + str(time.time()))
