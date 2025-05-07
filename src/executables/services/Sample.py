from executables.services.Base import BaseService
from resources.Globals import time

class Sample(BaseService):
    name = 'Sample'
    name_key = "_"
    interval = 10
    hidden = True

    def action(self):
        print('ping | time: ' + str(time.time()))
