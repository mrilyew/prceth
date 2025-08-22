class ArgsComparer():
    def __init__(self, comparing_options: dict, passed_options: dict, exc_type: str = "assert", is_free_settings: bool = False, rude_substitution: bool = False):
        self.compare = comparing_options
        self.args = passed_options
        self.impact = exc_type
        self.missing_args_inclusion = is_free_settings
        self.same_dict_mode = rude_substitution

    def dict(self):
        if self.same_dict_mode == True:
            return self.args

        output = {}

        # Do the compare thing

        hyb_options = dict(self.args)
        hyb_options.update(self.compare)

        # its just asks the names so we dont need to care about values
        for param_name, param_item in hyb_options.items():
            param_object = self.compare.get(param_name)
            if param_object == None and self.missing_args_inclusion == True:
                output[param_name] = self.args.get(param_name)
                continue

            param_object.configuration['name'] = param_name
            param_object.input_value(self.args.get(param_name))
            is_unexist = param_object.configuration.get('save_none_values', False)
            value = param_object.final_val()

            try:
                param_object.assertions()
                if value == None and is_unexist == False:
                    continue

                output[param_name] = value
            except Exception as _y:
                if self.impact == "assert":
                    raise _y
                else:
                    output[param_name] = param_object.default()

        return output
