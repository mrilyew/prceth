from declarable.Arguments.Argument import Argument

class ContentUnitArgument(Argument):
    def value(self):
        from db.Models.Content.ContentUnit import ContentUnit

        if self.passed_value != None:
            item = ContentUnit.ids(self.passed_value)

            return item
