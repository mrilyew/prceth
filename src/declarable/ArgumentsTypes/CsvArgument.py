from declarable.ArgumentsTypes.Argument import Argument

class CsvArgument(Argument):
    def value(self):
        if type(self.input_value) != list:
            __strs = self.input_value.split(",")

            return __strs
        else:
            return self.input_value

    def default(self):
        _def = super().default()

        if type(_def) == str:
            return _def.split(",")
        else:
            return _def
