from executables.services.Base import BaseService
from resources.Globals import time

class SSample(BaseService):
    name = 'SSample'
    name_key = "_"
    desc_key = "_"
    interval = 10
    hidden = True

    def action(self):
        print('ping | time: ' + str(time.time()))
