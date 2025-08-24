from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from db.Models.Content.ContentUnit import ContentUnit
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Findable import Findable
from executables.thumbnails import ThumbnailMethod
from declarable.ArgsComparer import ArgsComparer
from executables.acts import BaseAct
from executables.extractors import BaseExtractor
from utils.ClassProperty import classproperty
import importlib, pkgutil

class Representation(Runnable, Documentable, Findable):
    self_name = "Representation"
    cached_lists = {}

    @classproperty
    def extractors(cls):
        return cls.get_submodules("Extractors")

    @classproperty
    def acts(cls):
        return cls.get_submodules("Acts")

    @classmethod
    def get_submodule(cls, dir_name, submodule):
        _s = cls.get_submodules(dir_name)

        return _s[submodule]

    @classmethod
    def get_submodules(cls, dir_name):
        if cls.cached_lists.get(dir_name) != None:
            return cls.cached_lists[dir_name]

        if getattr(cls, "inherit_submodules", False) == True:
            return cls.__mro__[1].get_submodules(dir_name)

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

        cls.cached_lists[dir_name] = extractors_list

        return extractors_list

    @classmethod
    def declare_recursive(cls):
        return cls.sum_arguments(cls.extractors)

    @classmethod
    def sum_arguments(cls, extractors):
        _sum = {}
        for extractor_name, extractor_item in extractors.items():
            rec = extractor_item.declare_recursive()

            for name, item in rec.items():
                _sum[name] = item

        return _sum

    @classmethod
    def divide_arguments(cls, extractors):
        _sum = {}
        for extractor_name, extractor_item in extractors.items():
            _sum[extractor_name] = extractor_item.declare_recursive()

        return _sum

    @classmethod
    def find_suitable_extractor(cls, args):
        if getattr(cls, "extractor_wheel", None) != None:
            return cls.extractor_wheel(args)

        # dumb way
        all_extractors = cls.extractors
        for extractor_name, extractor_item in all_extractors.items():
            decls = extractor_item.declare_recursive()
            decl = ArgsComparer(decls, args)

            if decl.diff():
                return extractor_item

    @classmethod
    def get_variants(cls):
        pass

    @classmethod
    async def extract(cls, i: dict = {})->dict:
        extract_strategy = cls.find_suitable_extractor(i)
        assert extract_strategy != None, "cant find correct extractor"

        extract_strategy_instance = extract_strategy(cls)

        results = await extract_strategy_instance.safeExecute(i.copy())

        return results

    #class ContentUnit(ContentUnit):
        pass

    class AbstractAct(BaseAct):
        outer = None

        def __init__(self, outer):
            self.outer = outer

    class AbstractExtractor(BaseExtractor):
        buffer = {}
        args = {}

        def __init__(self, outer):
            self.outer = outer

        async def execute(self, i = {}):
            raise AbstractClassException("no action")

        def self_insert(self, item):
            item.mark_representation(self)

    class Thumbnail(ThumbnailMethod):
        pass
