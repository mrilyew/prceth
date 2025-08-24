from executables.representations import Representation
from declarable.Arguments import ObjectArgument
from utils.MainUtils import list_conversation

class Method(Representation.AbstractExtractor):
    def declare(cls):
        params = {}
        params["object"] = ObjectArgument({
            "type": "object",
        })

        return params

    async def execute(self, i = {}):
        json_object = list_conversation(i.get('object'))
        outs = []
        
        for i in json_object:
            out = self.ContentUnit()
            out.content = i

            outs.append(out)

        return outs

