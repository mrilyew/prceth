class Runnable:
    category = 'base'
    buffer = {}

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

    def self_insert(self, json_data: dict)->dict:
        '''
        You can append 'extractor' or 'representation' key there
        '''

        return json_data

    @classmethod
    def full_name(cls):
        return cls.category + '.' + cls.__name__

    def preExecute(self, i = {}):
        pass
