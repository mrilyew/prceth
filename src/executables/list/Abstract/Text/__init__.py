from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument, CsvArgument
from utils.MainUtils import proc_strtr

class Implementation(Representation):
    docs = {
        "name": "representations.abstract.text.name",
    }

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
            output = []

            for text in texts:
                out = self.ContentUnit()
                out.display_name = proc_strtr(text, 100)
                out.content = {
                    'text': text
                }

                output.append(out)

            return output

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByDefault'
