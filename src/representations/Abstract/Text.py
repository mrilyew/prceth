from representations.Representation import Representation
from resources.Descriptions import descriptions
from declarable.ArgumentsTypes import StringArgument

class Text(Representation):
    category = "Abstract"

    def declare():
        params = {}
        params["text"] = StringArgument({
            "default": None,
            "docs": {
                "definition": descriptions.get('__passed_text'),
            },
        })

        return params

    async def extractByDefault(self, i = {}):
        out = self.new_cu({
            'content': {
                'text': i.get('text')
            },
        })

        return [out]

    def extractWheel(self, i = {}):
        if 'text' in i:
            return 'extractByDefault'
