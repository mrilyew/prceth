class ArgsComparer():
    def __init__(self, comparing_options: dict, passed_options: dict, exc_type: str = "assert", is_free_settings: bool = False, rude_substitution: bool = False):
        self.compare = comparing_options # Argument class dict
        self.args = passed_options # what we got at input
        self.impact = exc_type # "assert": raise exceptions, "default": pass default on exception
        self.missing_args_inclusion = is_free_settings # Return the same value if argument didnt found in compared
        self.same_dict_mode = rude_substitution # Return input dict
        self.default_sub = True # Pass default value insted of None if None
        self.save_none_values = False # Save dict key even if None

    def diff(self):
        self.missing_args_inclusion = False
        self.default_sub = False
        _fin = 0

        for item_name, item_content in self.compare.items():
            if self.args.get(item_name) != None:
                _fin += 1

        return _fin > 0

    def dict(self):
        if self.same_dict_mode == True:
            return self.args

        output = {}

        # Do the compare thing

        hyb_options = dict(self.args)
        hyb_options.update(self.compare)

        # it just asks the names so we dont need to care about values
        for param_name, param_item in hyb_options.items():
            param_object = self.compare.get(param_name)
            if param_object == None:
                if self.missing_args_inclusion == True:
                    output[param_name] = self.args.get(param_name)

                continue

            param_object.configuration['name'] = param_name
            param_object.input_value(self.args.get(param_name))
            is_unexist = self.save_none_values
            value = param_object.val(self.default_sub)

            try:
                param_object.assertions()
                if value == None and is_unexist == False:
                    continue

                output[param_name] = value
            except Exception as _y:
                if self.impact == "assert":
                    raise _y
                else:
                    if self.default_sub == True:
                        output[param_name] = param_object.default()

        return output
