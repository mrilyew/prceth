from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from executables.RecursiveDeclarable import RecursiveDeclarable
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Saveable import Saveable
from executables.Findable import Findable
from executables.thumbnails import ThumbnailMethod
import importlib, pkgutil

class Representation(RecursiveDeclarable, Runnable, Documentable, Findable):
    hydrated = None
    self_name = "Representation"

    @classmethod
    def get_submodules(cls, dir_name):
        dirs = cls.__module__ + "." + dir_name
        extractors = importlib.import_module(dirs)
        extractors_list = {}

        for _, module_name, is_pkg in pkgutil.iter_modules(extractors.__path__):
            if not is_pkg:
                _imported = importlib.import_module(dirs + "." + module_name)
                extractors_list[module_name] = getattr(_imported, "Method")

        '''
        __methods = dir(cls)
        __out = []

        for __method in __methods:
            if __method.startswith(dir_name) == True:
                __out.append(getattr(cls, __method))
        '''

        return extractors_list

    @classmethod
    def get_extractors(cls):
        return cls.get_submodules("Extractors")

    @classmethod
    def get_acts(cls):
        return cls.get_submodules("Acts")

    @classmethod
    def sum_arguments(cls, extractors):
        _sum = {}
        for extractor_name, extractor_item in extractors.items():
            _sum[extractor_name] = extractor_item.declare_recursive()

        return _sum

    @classmethod
    def find_suitable_extractor(cls, args):
        if getattr(cls, "extractor_wheel", None) != None:
            return cls.extractor_wheel(args)

        # dumb way
        all_extractors = cls.get_extractors()
        all_arguments = cls.sum_arguments(all_extractors)

    @classmethod
    def get_variants(cls):
        pass

    @classmethod
    async def extract(cls, i: dict = {})->dict:
        extract_strategy = cls.find_suitable_extractor(i)
        assert extract_strategy != None, "couldn't find correct extractor"

        extract_strategy_instance = extract_strategy(cls)
        args = cls.validate(i.copy())

        extract_strategy_instance.preExecute(args)
        ress = await extract_strategy_instance.extract(i = args)

        for el in ress:
            el.unlisted = int(i.get('unlisted') == True)
            # el.representation = cls.full_name()

        return ress

    def hydrate(self, item):
        self.hydrated = item

        return self

    class AbstractAct(Runnable, Saveable, RecursiveDeclarable):
        pass

    class AbstractExtractor(Runnable, Saveable, RecursiveDeclarable):
        buffer = {}
        args = {}

        def __init__(self, outer):
            self.outer = outer

        async def execute(self, i = {}):
            raise AbstractClassException("no action")

        def self_insert(self, item):
            item.via_representation = self.outer

            return item

    class Thumbnail(ThumbnailMethod):
        pass
