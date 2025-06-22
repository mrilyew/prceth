from declarable.ArgumentsTypes.Argument import Argument

class IntArgument(Argument):
    def value(self)->int:
        try:
            return int(self.input_value)
        except ValueError:
            return None
