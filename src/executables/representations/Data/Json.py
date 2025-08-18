from executables.representations import Representation
from utils.MainUtils import parse_json, list_conversation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument

class Json(Representation):
    docs = {
        "name": "representations.data.json.name",
    }

    @classmethod
    def declare(cls):
        params = {}
        # мб не трогать
        params["object"] = ObjectArgument({
            "type": "object",
        })
        # todo make it csv
        params["text"] = StringArgument({})

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByText(self, i = {}):
            json_text = i.get('text')
            __obj = parse_json(json_text)

            out = self.ContentUnit()
            out.content = __obj

            return [out]

        async def extractByObject(self, i = {}):
            json_object = list_conversation(i.get('object'))
            outs = []
            
            for i in json_object:
                out = self.ContentUnit()
                out.content = i

                outs.append(out)

            return outs

        def extractWheel(self, i = {}):
            if 'object' in i:
                return 'extractByObject'
            elif 'text' in i:
                return 'extractByText'
