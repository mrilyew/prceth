class Runnable:
    category = 'base'
    buffer = {}
    available = ['web', 'cli']

    # Comparisons

    @classmethod
    def isAbstract(cls):
        return cls.category.lower() in ["template", "base"]

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
