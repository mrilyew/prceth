from declarable.ArgumentsTypes.Argument import Argument
import json5

class JsonArgument(Argument):
    def value(self):
        if type(self.input_value) == str:
            return json5.loads(self.input_value)
        else:
            return self.input_value
