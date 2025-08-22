from declarable.Arguments.Argument import Argument
import json5

class JsonArgument(Argument):
    def value(self):
        if type(self.passed_value) == str:
            return json5.loads(self.passed_value)
        else:
            return self.passed_value
