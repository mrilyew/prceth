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

    def default(self):
        _def = super().default()

        if type(_def) == str:
            return _def.split(",")
        else:
            return _def
