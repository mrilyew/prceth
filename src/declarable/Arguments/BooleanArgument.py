from declarable.Arguments.Argument import Argument

class BooleanArgument(Argument):
    def value(self):
        return int(self.passed_value) == 1
