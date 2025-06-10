from declarable.ArgumentsTypes.Argument import Argument

class CsvArgument(Argument):
    def value(self):
        if type(self.input_value) != list:
            __strs = self.input_value.split(",")

            return __strs
        else:
            return self.input_value
