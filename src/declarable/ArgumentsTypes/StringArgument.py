from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import proc_strtr

class StringArgument(Argument):
    def get_maxlength(self):
        return self.data.get('maxlength', None)

    def value(self)->str:
        if self.get_maxlength() != None:
            return proc_strtr(str(self.input_value), int(self.data.get("maxlength")), multipoint=False)
        else:
            return str(self.input_value)
