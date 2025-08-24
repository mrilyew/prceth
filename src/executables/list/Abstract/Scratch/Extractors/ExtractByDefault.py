from executables.representations import Representation
from declarable.Arguments import StringArgument

class Method(Representation.AbstractExtractor):
    async def execute(self, i = {}):
        out = self.ContentUnit()
        out.content = i

        return [out]
