from resources.Exceptions import AbstractClassException
from executables.Runnable import Runnable
from resources.Exceptions import SuitableExtractMethodNotFound
from app.App import logger

class Representation(Runnable):
    category = "base"

    async def extract(self, i = {}):
        __wheel = self.extractWheel(i)
        if __wheel == None:
            __wheel = ""

        __wheel_method = getattr(self, __wheel, None)
        if __wheel_method == None:
            raise SuitableExtractMethodNotFound('Not found suitable extractor for current args')

        __res = await __wheel_method(i)

        return __res

    def extractWheel(self):
        raise AbstractClassException("This is abstract representation")

    async def safeExtract(self, i: dict = {})->dict:
        __args = self.validate(i)
        __res = await self.extract(i=__args)

        return __res

    @classmethod
    def rawListMethods(cls):
        fourbidden = ["canBeExecuted", "common_category", "extract", "isAbstract", "rawListMethods"]
        __methods = dir(cls)
        __out = []
        
        for __method in __methods:
            if __method.startswith("__") == False and __method.startswith("extract") == False and __method not in fourbidden:
                __out.append(__method)

        return __out

    def self_insert(self, json_data: dict):
        json_data['representation'] = self.full_name

        return json_data
