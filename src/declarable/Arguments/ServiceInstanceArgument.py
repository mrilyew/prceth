from declarable.Arguments.Argument import Argument

class ServiceInstanceArgument(Argument):
    def value(self):
        from db.Models.Instances.ServiceInstance import ServiceInstance

        if self.passed_value != None:
            item = ServiceInstance.get(self.input_value)

            return item
