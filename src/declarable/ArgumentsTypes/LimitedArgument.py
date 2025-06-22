from declarable.ArgumentsTypes.Argument import Argument

class LimitedArgument(Argument):
    def value(self):
        __allowed = self.data.get("values")
        inp = str(self.input_value)
        if len(inp) == 0:
            if self.data.get('return_none_on_empty', True) == True:
                return None

        assert inp in __allowed, f"not valid value, {self.data.get('name')}={self.input_value}"

        return inp
