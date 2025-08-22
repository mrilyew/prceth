from declarable.Arguments.Argument import Argument

class ActArgument(Argument):
    def value(self):
        from executables.acts import Act

        return Act.findByName(str(self.passed_value))
