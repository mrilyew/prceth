from executables.representations import Representation
from db.Models.Content.ContentUnit import ContentUnit

class Scratch(Representation):
    docs = {
        "name": "representations.abstract.scratch.name",
    }
    executable_cfg =  {
        'free_args': True
    }

    class Extractor(Representation.ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = self.ContentUnit()
            out.content = i

            return [out]

        def extractWheel(self, i = {}):
            return 'extractByDefault'
