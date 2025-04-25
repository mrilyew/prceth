class DeclarableArgs():
    def __init__(self, compare_params: dict, out_args: dict, exc_type: str = "assert", is_free_settings: bool = False):
        self.params = compare_params
        self.args = out_args
        self.exc_type = exc_type
        self.is_free_settings = is_free_settings

    def recieveObjectByName(self, param_name: str):
        param_object = self.params.get(param_name)

        return param_object

    def recieveValue(self, param_name: str, param_object: object):
        from resources.Globals import utils

        if param_object == None:
            if self.is_free_settings == True:
                return __value
        
        __value = self.args.get(param_name, param_object.get("default"))
        
        if __value != None:
            match(param_object.get("type")):
                case "int":
                    __value = int(__value)
                case "float":
                    __value = float(__value)
                case "array":
                    __allowed = param_object.get("values")
                    assert __value in __allowed, f"not valid value, {param_name}={__value}"
                    if __value == None:
                        __value = param_object.get("default")
                case "string":
                    if param_object.get("maxlength") != None:
                        __value = utils.proc_strtr(str(__value), int(param_object.get("maxlength")), multipoint=False)
                    else:
                        __value = str(__value)
                case "object":
                    if type(__value) == str:
                        __value = utils.parse_json(__value)
                    elif type(__value) == dict or type(__value) == object:
                        if param_object.get("default") != None:
                            __value = param_object.get("default")
                        else:
                            __value = None
                case "bool":
                    __value = int(__value) == 1
                case _:
                    pass

            return __value
        else:
            if param_object.get("default") != None:
                return param_object.get("default")

        # Asserting for value is not null
        if param_object.get("assertion") != None:
            __assertion = param_object.get("assertion")

            if __assertion.get("assert_not_null") == True:
                assert __value != None, f"{param_name} not passed"

            if __assertion.get("assert_link") != None:
                new_param_name = __assertion.get("assert_link")
                new_param_object = self.params.get(new_param_name)

                assert __value != None or self.args.get(new_param_name, new_param_object.get("default")) != None, f"{new_param_name} or {param_name} not passed"

    def dict(self):
        __dict = {}

        if self.is_free_settings == True:
            for index, param_name in enumerate(self.args):
                __dict[param_name] = self.args.get(param_name)
        else:
            for index, param_name in enumerate(self.params):
                param_object = self.recieveObjectByName(param_name)

                try:
                    __dict[param_name] = self.recieveValue(param_name, param_object)
                except Exception as _y:
                    print(_y)
                    if self.exc_type == "assert":
                        raise _y
                    else:
                        __dict[param_name] = param_object.get("default")

        return __dict
