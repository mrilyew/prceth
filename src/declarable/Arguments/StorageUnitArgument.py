from declarable.Arguments.Argument import Argument

class StorageUnitArgument(Argument):
    def value(self):
        from db.Models.Content.StorageUnit import StorageUnit

        if self.passed_value != None:
            item = StorageUnit.ids(self.passed_value)

            return item
