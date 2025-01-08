from resources.globals import consts, Path, utils

class BaseAct:
    name = 'base'
    category = 'base'
    allow_type = 'entity'
    type = 'string'

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def cleanup(self, entity):
        pass

    def cleanup_fail(self):
        pass
    
    def execute(self, args):
        pass

    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "allow": self.allow_type,
        }
