from utils.ClassProperty import classproperty
import importlib, pkgutil

class Submodulable():
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

        # todo
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
