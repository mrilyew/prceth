from services.Base import BaseService
from resources.globals import time

class sample(BaseService):
    name = 'sample'
    name_key = "_"
    desc_key = "_"
    interval = 10
    hidden = True

    def action(self):
        print('ping | time: ' + str(time.time()))
