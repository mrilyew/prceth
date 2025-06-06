from resources.Exceptions import AbstractClassException
from executables.Runnable import Runnable

class Representation(Runnable):
    category = "base"

    def extract(self, i = {}):
        __wheel = self.extractWheel()
        
        return getattr(self, __wheel)()

    def extractWheel(self):
        raise AbstractClassException("This is abstract representation")

    @classmethod
    def rawListMethods(cls):
        fourbidden = ["canBeExecuted", "common_category", "extract", "isAbstract", "rawListMethods"]
        __methods = dir(cls)
        __out = []
        
        for __method in __methods:
            if __method.startswith("__") == False and __method.startswith("extract") == False and __method not in fourbidden:
                __out.append(__method)

        return __out
