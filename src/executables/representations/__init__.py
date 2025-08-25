from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from executables.Documentable import Documentable
from executables.Runnable import Runnable
from executables.Findable import Findable
from executables.Submodulable import Submodulable
from executables.thumbnails import ThumbnailMethod
from declarable.ArgsComparer import ArgsComparer
from executables.extractors import BaseExtractor
from executables.acts import BaseAct

class Representation(Runnable, Documentable, Findable, Submodulable):
    self_name = "Representation"

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
