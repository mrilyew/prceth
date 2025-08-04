from declarable.ArgumentsTypes.Argument import Argument
from utils.MainUtils import parse_json

class ContentUnitArgument(Argument):
    def value(self):
        from db.Models.Content.ContentUnit import ContentUnit

        if self.input_value != None:
            item = ContentUnit.ids(self.input_value)

            return item
