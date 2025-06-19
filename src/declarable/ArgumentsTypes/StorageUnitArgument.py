from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import parse_json

class StorageUnitArgument(Argument):
    def value(self):
        from db.Content.StorageUnit import StorageUnit

        if self.input_value != None:
            item = StorageUnit.ids(self.input_value)
            if item == None:
                return None

            return item
