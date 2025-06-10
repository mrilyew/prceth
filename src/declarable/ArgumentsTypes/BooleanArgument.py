from declarable.ArgumentsTypes.Argument import Argument

class BooleanArgument(Argument):
    def value(self)->bool:
        if type(self.input_value) == bool:
            return self.input_value
        else:
            return int(self.input_value) == 1
