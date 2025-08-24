from declarable.Arguments.Argument import Argument
from executables.Findable import Findable

class ExecutableArgument(Argument):
    def value(self):
        return Findable.findByName(str(self.passed_value), True)
