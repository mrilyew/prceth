from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument, CsvArgument
from db.DbInsert import db_insert
from utils.MainUtils import proc_strtr

class Text(Representation):
    category = "Abstract"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = CsvArgument({
            "orig": StringArgument({
                "is_long": True,
            }),
            "default": None,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByDefault(self, i = {}):
            texts = i.get('text')
            out_arr = []

            for text in texts:
                name = proc_strtr(text, 100)

                out = db_insert.contentFromJson({
                    'name': name,
                    'content': {
                        'text': text
                    },
                })
                out_arr.append(out)

            return out_arr

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByDefault'
