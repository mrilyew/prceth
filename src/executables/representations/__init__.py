from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from executables.RecursiveDeclarable import RecursiveDeclarable
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Saveable import Saveable

class Representation(RecursiveDeclarable, Runnable, Documentable):
    category = "base"
    hydrated = None

    @classmethod
    async def extract(cls, i: dict = {})->dict:
        if getattr(cls, 'Extractor', None) == None:
            raise AbstractClassException('ExecutableStrategy is not implemented at this class')

        strategy = cls.Extractor(cls)
        args = cls.validate(i.copy())

        strategy.preExecute(args)

        return await strategy.extract(i = args)

    @classmethod
    def rawListMethods(cls):
        fourbidden = ["canBeExecuted", "common_category", "extract", "isAbstract", "rawListMethods"]
        __methods = dir(cls)
        __out = []

        for __method in __methods:
            if __method.startswith("__") == False and __method not in fourbidden:
                __out.append(__method)

        return __out

    def hydrate(self, item):
        self.hydrated = item

        return self

    class ExtractStrategy(Runnable, Saveable):
        buffer = {}
        args = {}

        def __init__(self, outer):
            self.outer = outer

        def extractWheel(self, i = {}):
            raise AbstractClassException("This is abstract representation")

        async def extract(self, i = {}):
            __wheel = self.extractWheel(i)
            if __wheel == None:
                __wheel = ""

            __wheel_method = getattr(self, __wheel, None)
            if __wheel_method == None:
                raise SuitableExtractMethodNotFound('Not found suitable extractor for current args')

            self.args = i

            __res = await __wheel_method(i)

            return __res

        def self_insert(self, json_data: dict):
            json_data['representation'] = self.outer.full_name()
            json_data['representation_class'] = self

            return json_data
