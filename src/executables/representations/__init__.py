from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from db.Models.Content.ContentUnit import ContentUnit
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Saveable import Saveable
from executables.Findable import Findable
from executables.thumbnails import ThumbnailMethod
from executables.acts import BaseAct
from executables.extractors import BaseExtractor
from utils.ClassProperty import classproperty
import importlib, pkgutil

class Representation(Runnable, Documentable, Findable):
    self_name = "Representation"
    cached_lists = {}

    @classproperty
    def extractors(cls):
        if cls.cached_lists.get("Extractors") == None:
            cls.cached_lists["Extractors"] = cls.get_submodules("Extractors")

        return cls.cached_lists.get("Extractors")

    @classproperty
    def acts(cls):
        if cls.cached_lists.get("Acts") == None:
            cls.cached_lists["Acts"] = cls.get_submodules("Acts")

        return cls.cached_lists.get("Acts")

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
        all_extractors = cls.extractors
        for extractor_name, extractor_item in all_extractors.items():
            decls = extractor_item.declare_recursive()

            if decls:
                pass

    @classmethod
    def get_variants(cls):
        pass

    @classmethod
    async def extract(cls, i: dict = {})->dict:
        extract_strategy = cls.find_suitable_extractor(i)
        assert extract_strategy != None, "couldn't find correct extractor"

        extract_strategy_instance = extract_strategy(cls)
        args = extract_strategy_instance.validate(i.copy())

        extract_strategy_instance.before_execute(args)
        results = await extract_strategy_instance.extract(i = args)

        return results

    class ContentUnit(ContentUnit):
        pass

    class AbstractAct(BaseAct):
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
            item.via_representation = self.outer

            return item

    class Thumbnail(ThumbnailMethod):
        pass
