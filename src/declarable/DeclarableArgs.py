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


        is_free_settings: there will be passed every arg if it missing in compare dict

        rude_substitution: this will be just same dict on return
        '''
        self.comparing = comparing_options
        self.args = passed_options
        self.impact = exc_type
        self.is_free_settings = is_free_settings
        self.substitution = rude_substitution

    def recieveObjectByName(self, param_name: str):
        return self.comparing.get(param_name)

    def dict(self):
        output = {}

        if self.substitution == True:
            # probaly just return the same dict?? lol
            for index, param_name in enumerate(self.args):
                output[param_name] = self.args.get(param_name)

            return output

        __enumeration = self.comparing
        if self.is_free_settings:
            for a, n in enumerate(self.args):
                __enumeration[n] = self.comparing.get(n)

        for index, param_name in enumerate(__enumeration):
            param_object = self.recieveObjectByName(param_name)
            if param_object == None and self.is_free_settings == True:
                output[param_name] = self.args.get(param_name)
                continue

            param_object.passValue(self.args.get(param_name))
            param_object.data['name'] = param_name
            is_unexist = param_object.data.get('save_none_values', False)
            value = None

            try:
                value = param_object.val()
            except:
                value = param_object.default()

            try:
                param_object.assertions(value)
                param_object.special_assertions(value)

                if value == None and is_unexist == False:
                    continue

                output[param_name] = value
            except Exception as _y:
                if self.impact == "assert":
                    raise _y
                else:
                    output[param_name] = param_object.default()

        for index, param_name in enumerate(output):
            param_object = self.recieveObjectByName(param_name)

            if param_object != None:
                param_object.conditions_assertions(output)

        return output
