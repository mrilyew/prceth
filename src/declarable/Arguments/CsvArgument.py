from declarable.Arguments.Argument import Argument
from utils.MainUtils import is_valid_json
import json

class CsvArgument(Argument):
    def value(self):
        intrerm_val = []
        end_vals = []

        if type(self.passed_value) == list:
            intrerm_val = self.passed_value

        if type(self.passed_value) == str:
            is_json = is_valid_json(self.passed_value)

            if is_json == False:
                intrerm_val = self.passed_value.split(",")
            else:
                _json = json.loads(self.passed_value)

                if type(_json) == list:
                    intrerm_val = _json

        for val in intrerm_val:
            if self.configuration.get("orig") != None:
                p = self.configuration.get("orig")
                p.input_value(val)

                end_vals.append(p.val())
            else:
                end_vals.append(val)

        return end_vals

    def describe(self):
        orig_out = super().describe()
        if orig_out.get("orig") != None and type(orig_out.get("orig")) != str:
            orig_out["orig"] = orig_out.get("orig").describe()

        return orig_out

    def default(self):
        _def = super().default()

        if type(_def) == str:
            return _def.split(",")
        else:
            return _def

    def get_list_argument_type(self):
        return self.configuration.get('argument_type')
