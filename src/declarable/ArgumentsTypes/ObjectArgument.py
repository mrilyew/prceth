from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import parse_json

class ObjectArgument(Argument):
    def value(self):
        if type(self.input_value) == list:
            return self.input_value
        elif type(self.input_value) == str:
            return parse_json(self.input_value)
        elif type(self.input_value) == dict or type(self.input_value) == object:
            return self.input_value
