from declarable.ArgumentsTypes.Argument import Argument

class LimitedArgument(Argument):
    def value(self):
        inp = str(self.input_value)
        if len(inp) == 0:
            if self.data.get('return_none_on_empty', True) == True:
                return self.default()

        return inp

    def special_assertions(self, inp):
        __allowed = self.data.get("values")

        assert inp in __allowed, f"not valid value, {self.data.get('name')}={self.input_value}"
