from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import proc_strtr

class ActArgument(Argument):
    def value(self)->str:
        from executables.acts import Act

        inp = str(self.input_value)
        act_class = Act.findByName(inp)

        return act_class
