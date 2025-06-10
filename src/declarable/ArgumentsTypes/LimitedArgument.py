from declarable.ArgumentsTypes.Argument import Argument

class LimitedArgument(Argument):
    def value(self):
        __allowed = self.data.get("values")
        assert self.input_value in __allowed, f"not valid value, {self.data.get('name')}={self.input_value}"

        return self.input_value
