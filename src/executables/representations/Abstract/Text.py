from executables.representations.Representation import Representation
from declarable.ArgumentsTypes import StringArgument
from executables.representations.ExtractStrategy import ExtractStrategy
from db.DbInsert import db_insert

class Text(Representation):
    category = "Abstract"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({
            "default": None,
        })

        return params

    class Extractor(ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = db_insert.contentFromJson({
                'content': {
                    'text': i.get('text')
                },
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByDefault'
