from resources.globals import config
from db.collection import Collection

class Api():
    def __init__(self):
        self.ctx = "cli"

    def setOption(self, option_name, option_value):
        config.set(option_name, option_value)

        return True
    
    def getOption(self, option_name):
        return config.get(option_name)
    
    def resetOptions(self):
        return config.reset()
    
    def getAllOptions(self):
        return config.data
    
    def createCollection(self, params):
        print(params)
        return

api = Api()
