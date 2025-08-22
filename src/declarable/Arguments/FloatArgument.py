from declarable.Arguments.Argument import Argument

class FloatArgument(Argument):
    def value(self)->float:
        return float(self.passed_value)
