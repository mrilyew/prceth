from declarable.ArgumentsTypes.Argument import Argument

class IntArgument(Argument):
    def value(self)->int:
        return int(self.input_value)
