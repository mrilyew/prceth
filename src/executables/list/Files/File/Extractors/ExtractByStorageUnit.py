from declarable.Arguments import CsvArgument, StorageUnitArgument
from executables.representations import Representation

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["storage_unit"] = CsvArgument({
            "orig": StorageUnitArgument({}),
            "docs": {
                "name": "representations.data.file.storage_unit.name"
            },
            "default": None,
        })

        return params

    async def execute(self, i = {}):
        su = i.get('storage_unit')
        outs = []

        for item in su:
            out = self.ContentUnit()

            out.add_link(item)
            out.set_common_link(item)
            out = await self.process_item(out)

            outs.append(out)

        return outs
