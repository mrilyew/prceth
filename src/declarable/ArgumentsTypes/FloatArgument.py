from declarable.ArgumentsTypes.Argument import Argument

class FloatArgument(Argument):
    def value(self)->float:
        return float(self.input_value)
