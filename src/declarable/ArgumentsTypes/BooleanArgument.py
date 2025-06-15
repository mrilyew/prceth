from declarable.ArgumentsTypes.Argument import Argument

class BooleanArgument(Argument):
    def value(self):
        return int(self.input_value) == 1
