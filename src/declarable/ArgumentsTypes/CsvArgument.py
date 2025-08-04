from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import is_valid_json
import json

class CsvArgument(Argument):
    def value(self):
        val = self.input_value

        if type(val) != list:
            is_json = is_valid_json(val)

            if is_json == False:
                return val.split(",")
            else:
                _json = json.loads(val)

                if type(_json) == list:
                    return _json
        else:
            return val

    def out(self):
        orig_out = super().out()
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
        return self.data.get('argument_type')
