from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import parse_json

class StorageUnitArgument(Argument):
    def value(self):
        from db.StorageUnit import StorageUnit

        if self.input_value != None:
            return StorageUnit.get(self.input_value)
