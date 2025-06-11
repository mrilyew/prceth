from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import parse_json

class JsonArgument(Argument):
    def value(self):
        return parse_json(self.input_value)
