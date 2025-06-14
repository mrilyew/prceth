from declarable.ArgsValidator import ArgsValidator

class RecursiveDeclarable:
    executable_cfg =  {}

    def define():
        '''
        Define consts, temp variables etc
        '''
        pass

    @classmethod
    def validate(cls, args: dict)->dict:
        return ArgsValidator().validate(cls.declare_recursive(), args, cls.executable_cfg)

    def declare():
        '''
        Method that defines dictionary of current executable args
        '''
        params = {}

        return params

    @classmethod
    def declare_recursive(cls):
        '''
        Brings all params from parent classes to one dict
        '''
        ignore_list = cls.executable_cfg.get('ignore', [])
        output_params = {}

        for __sub_class in cls.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            if hasattr(__sub_class, "define") == True:
                __sub_class.define()

            intermediate_dict = {}
            current_level_declaration = __sub_class.declare()
            for i, name in enumerate(current_level_declaration):
                if name in ignore_list:
                    continue

                intermediate_dict[name] = current_level_declaration.get(name)

            output_params.update(intermediate_dict)

        return output_params
