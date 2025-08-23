from declarable.Arguments import CsvArgument, StorageUnitArgument
from executables.representations import Representation

keys = {
    "storage_unit.name": {
        "en_US": "Storage unit ID"
    }
}

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["storage_unit"] = CsvArgument({
            "orig": StorageUnitArgument({}),
            "docs": {
                "name": keys.get("storage_unit.name")
            },
            "assertion": {
                "not_null": True
            }
        })

        return params

    async def execute(self, i = {}):
        su = i.get('storage_unit')
        outs = []

        for item in su:
            if item == None:
                continue

            out = self.ContentUnit()

            out.add_link(item)
            out.set_common_link(item)
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
