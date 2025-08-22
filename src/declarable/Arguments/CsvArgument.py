from declarable.Arguments.Argument import Argument
from utils.MainUtils import is_valid_json
import json

class CsvArgument(Argument):
    def value(self):
        val = self.passed_value
        intrerm_val = []
        end_vals = []

        if type(val) == list:
            intrerm_val = val

        if type(val) == str:
            is_json = is_valid_json(val)

            if is_json == False:
                intrerm_val = val.split(",")
            else:
                _json = json.loads(val)

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
            orig_out["orig"] = orig_out.get("orig").out()

        return orig_out

    def default(self):
        _def = super().default()

        if type(_def) == str:
            return _def.split(",")
        else:
            return _def

    def get_list_argument_type(self):
        return self.configuration.get('argument_type')
