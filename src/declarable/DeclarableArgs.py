from utils.MainUtils import proc_strtr, parse_json

class DeclarableArgs():
    '''
    Class thats represents declarative arguments.\n

    Takes input params and total list of params.\n

    Methods:\n
    recieveObjectByName()\n
    recieveValue()\n
    dict()\n
    '''

    def __init__(self, comparing_options: dict, passed_options: dict, exc_type: str = "assert", is_free_settings: bool = False, rude_substitution: bool = False):
        '''
        compare_params: total declared params

        out_args: input dict of params that will be compared with total params

        exc_type:

        "assert" — AssertException will be risen on exception (when \"type\" is \"array\")

        "ignore" — Default value will be set on exception

        is_free_settings: Values from passed args will be set
        '''
        self.comparing = comparing_options
        self.args = passed_options
        self.exc_type = exc_type
        self.is_free_settings = is_free_settings
        self.substitution = rude_substitution

    def recieveObjectByName(self, param_name: str):
        return self.comparing.get(param_name)

    def dict(self):
        __dict = {}

        if self.substitution == True:
            for index, param_name in enumerate(self.args):
                __dict[param_name] = self.args.get(param_name)

            return __dict

        __enumeration = self.comparing
        if self.is_free_settings:
            for a, n in enumerate(self.args):
                __enumeration[n] = self.comparing.get(n)

        for index, param_name in enumerate(__enumeration):
            param_object = self.recieveObjectByName(param_name)
            if param_object == None and self.is_free_settings == True:
                __dict[param_name] = self.args.get(param_name)
                continue

            param_object.passValue(self.args.get(param_name))
            param_object.data['name'] = param_name

            try:
                __unexist = param_object.data.get('save_none_values', False)
                __value = param_object.val()

                param_object.assertions(__value)

                if __value == None and __unexist == False:
                    continue

                __dict[param_name] = __value
            except Exception as _y:
                if self.exc_type == "assert":
                    raise _y
                else:
                    __dict[param_name] = param_object.default()

        return __dict
