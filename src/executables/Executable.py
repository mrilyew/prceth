from resources.Globals import storage, utils
from db.Entity import Entity

class Executable:
    name = 'base'
    category = 'template'
    passed_params = {}
    params = {}
    temp_dirs = []
    manual_params = False

    def declare():
        params = {}

        return params
    
    def recursiveDeclare(self):
        for __sub_class in self.__class__.__mro__:
            if hasattr(__sub_class, "declare") == False:
                continue

            new_params = __sub_class.declare()
            self.params.update(new_params)
        
    def setArgs(self, args):
        self.params = {}
        
        # Catching params from parent extractors
        self.recursiveDeclare()
        
        MAX_OUTPUT_CHECK_PARAMS = self.params
        if MAX_OUTPUT_CHECK_PARAMS == None:
            return
        
        for index, param_name in enumerate(MAX_OUTPUT_CHECK_PARAMS):
            param_object = MAX_OUTPUT_CHECK_PARAMS.get(param_name)
            __value = args.get(param_name, param_object.get("default"))
            if __value != None:
                match(param_object.get("type")):
                    case "int":
                        __value = int(__value)
                    case "float":
                        __value = float(__value)
                    case "array":
                        __allowed = param_object.get("values")
                        assert __value in __allowed, "not valid value"
                        if __value == None:
                            __value = param_object.get("default")
                    case "string":
                        if param_object.get("maxlength") != None:
                            __value = utils.proc_strtr(str(__value), int(param_object.get("maxlength")), multipoint=False)
                        else:
                            __value = str(__value)
                    case "object":
                        if type(__value) in ["dict", "array"] == False:
                            if param_object.get("default") != None:
                                __value = param_object.get("default")
                            else:
                                __value = None
                    case "bool":
                        __value = int(__value) == 1
                    case _:
                        break
                
                self.passed_params[param_name] = __value
            else:
                if param_object.get("default") != None:
                    self.passed_params[param_name] = param_object.get("default")

            if param_object.get("assertion") != None:
                __assertion = param_object.get("assertion")
                
                if __assertion.get("assert_not_null") == True:
                    assert __value != None, f"{param_name} not passed"

                if __assertion.get("assert_link") != None:
                    new_param_name = __assertion.get("assert_link")
                    new_param_object = MAX_OUTPUT_CHECK_PARAMS.get(new_param_name)

                    assert __value != None or args.get(new_param_name, new_param_object.get("default")) != None, f"{new_param_name} or {param_name} not passed"
        
        if self.manual_params == True:
            self.passed_params.update(args)
            
    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
            "params": getattr(self, "params", {})
        }

    def allocateTemp(self):
        _dir = storage.makeTemporaryCollectionDir(self.temp_dir_prefix)
        self.temp_dirs.append(_dir)

        return _dir
