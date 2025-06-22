from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import proc_strtr

class StringArgument(Argument):
    def get_maxlength(self):
        return self.data.get('maxlength', None)

    def value(self)->str:
        inp = str(self.input_value)
        if len(inp) == 0:
            if self.data.get('return_none_on_empty', True) == True:
                return None

        if self.get_maxlength() != None:
            return proc_strtr(inp, int(self.data.get("maxlength")), multipoint=False)
        else:
            return inp
