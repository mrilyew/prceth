from representations.Representation import Representation
from resources.Descriptions import descriptions
from declarable.ArgumentsTypes import StringArgument
from representations.ExtractStrategy import ExtractStrategy

class Text(Representation):
    category = "Abstract"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({
            "default": None,
            "docs": {
                "definition": descriptions.get('__passed_text'),
            },
        })

        return params

    class Extractor(ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = self.contentUnit({
                'content': {
                    'text': i.get('text')
                },
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByDefault'
