from executables.acts import Act
from declarable.ArgumentsTypes import CsvArgument, IntArgument
from db.Models.Content.ContentUnit import ContentUnit

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["ids"] = CsvArgument({
            "orig": IntArgument({}),
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        ids = i.get("ids")

        items = ContentUnit.ids(ids)

        fnl = []
        
        for item in items:
            fnl.append(item.api_structure())

        return fnl
