class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class Runnable:
    buffer = {}
    base_categories = ["template", "base"]
    available = ['web', 'cli']

    @classproperty
    def category(self)->str:
        class_full_name = self.__module__
        _ = class_full_name.split('.')

        return _[-2]

    # Comparisons

    @classmethod
    def isAbstract(cls):
        return cls.category.lower() in cls.base_categories

    @classmethod
    def isHidden(cls):
        return getattr(cls, "hidden", False) == True

    @classmethod
    def canBeExecuted(cls):
        '''
        Is this Executable can be runned or it's technical
        '''
        return cls.isAbstract() == False and cls.isHidden() == False

    @classmethod
    def isConfirmable(cls):
        return getattr(cls, "PreExecute", None)

    @classmethod
    def full_name(cls):
        return cls.category + '.' + cls.__name__

    def preExecute(self, i = {}):
        pass
