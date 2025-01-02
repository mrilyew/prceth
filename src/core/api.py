from resources.globals import config

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

api = Api()
