from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument
from db.DbInsert import db_insert
from utils.MainUtils import proc_strtr

class Text(Representation):
    category = "Abstract"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({
            "default": None,
            "is_long": True,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByDefault(self, i = {}):
            text = i.get('text')
            name = proc_strtr(text, 100)

            out = db_insert.contentFromJson({
                'name': name,
                'content': {
                    'text': text
                },
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByDefault'
