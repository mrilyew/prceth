from executables.representations import Representation
from utils.MainUtils import parse_json, list_conversation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from db.DbInsert import db_insert

class Json(Representation):
    docs = {
        "name": "representations.data.json.name",
    }

    @classmethod
    def declare(cls):
        params = {}
        params["object"] = ObjectArgument({
            "type": "object",
        })
        params["text"] = StringArgument({})

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByText(self, i = {}):
            json_text = i.get('text')
            __obj = parse_json(json_text)

            out = db_insert.contentFromJson({
                'content': __obj,
            })

            return [out]

        async def extractByObject(self, i = {}):
            json_object = list_conversation(i.get('object'))
            out = []
            
            for i in json_object:
                out.append(db_insert.contentFromJson({
                    'content': i,
                }))

            return out

        def extractWheel(self, i = {}):
            if 'object' in i:
                return 'extractByObject'
            elif 'text' in i:
                return 'extractByText'
