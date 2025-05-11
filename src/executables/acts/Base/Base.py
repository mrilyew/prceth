from db.Collection import Collection
from db.Entity import Entity
from db.File import File
from executables.Executable import Executable

class BaseAct(Executable):
    name = 'base'
    category = 'base'
    accepts = 'entity'

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def parseMainInput(self, main_input):
        try:
            if main_input == None:
                return None
            if self.accepts == "string":
                return main_input
            
            ____split = main_input.split("_", 1)
            if len(____split) == 1:
                ____split = (self.accepts, ____split[0])

            p1, p2 = ____split

            if p1 not in ["entity", "collection", "both"]:
                return None

            if p1 == "entity":
                if self.accepts not in ["entity", "both"]:
                    return None
                
                __ent = Entity.get(int(p2))
                return __ent
            elif p1 == "collection":
                if self.accepts not in ["collection", "both"]:
                    return None
                
                __ent = Collection.get(int(p2))
                return __ent
            elif p1 == "file":
                if self.accepts != "file":
                    return None
                
                __ent = File.get(int(p2))
                return __ent
        except Exception as __e:
            print(__e)
            return None
        
    def cleanup(self, entity):
        pass
    
    async def execute(self, i, args):
        return {}

    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "allow": self.accepts,
        }
