from declarable.Arguments.Argument import Argument
from utils.MainUtils import proc_strtr

class StringArgument(Argument):
    def get_maxlength(self):
        return self.configuration.get('maxlength', None)

    def value(self)->str:
        inp = str(self.passed_value)
        if len(inp) == 0:
            if self.configuration.get('return_none_on_empty', True) == True:
                return self.default()

        if self.get_maxlength() != None:
            return proc_strtr(inp, int(self.configuration.get("maxlength")), multipoint=False)
        else:
            return inp
