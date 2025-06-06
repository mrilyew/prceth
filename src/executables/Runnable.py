from declarable.ArgsValidator import ArgsValidator

class Runnable:
    name = 'base'
    category = 'base'

    docs = {
        "name": {
            "en": "Abstract name"
        },
        "definition": {
            "en": "Abstract description"
        }
    }
    declaration_cfg =  {}

    # Arguments

    def defineConsts(self):
        pass

    def declare():
        '''
        Method that defines dictionary of current executable args
        '''
        params = {}

        return params

    def recursiveDeclaration(self):
        '''
        Brings all params from parent classes to one dict
        '''
        ignore_list = self.declaration_cfg.get('ignore', [])
        output_params = {}

        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            intermediate_dict = {}
            current_level_declaration = __sub_class.declare()
            for i, name in enumerate(current_level_declaration):
                if name in ignore_list:
                    continue

                intermediate_dict[name] = current_level_declaration.get(name)

            output_params.update(intermediate_dict)

        return output_params

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

    def validate(self, args: dict)->dict:
        return ArgsValidator().validate(self.recursiveDeclaration(), args, self.declaration_cfg)
