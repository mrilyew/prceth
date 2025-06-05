from resources.Exceptions import AbstractClassException

class Representation:
    common_category = "none"

    def extract(self, i = {}):
        self.extractWheel()

    def extractWheel(self):
        raise AbstractClassException("This is abstract representation")

    @classmethod
    def listMethods(self):
        pass
