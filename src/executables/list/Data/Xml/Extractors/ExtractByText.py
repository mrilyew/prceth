from executables.representations import Representation
from declarable.Arguments import StringArgument
from utils.MainUtils import parse_json

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({})

        return params

    async def execute(self, i = {}):
        json_text = i.get('text')
        __obj = parse_json(json_text)

        out = self.ContentUnit()
        out.content = __obj

        return [out]
