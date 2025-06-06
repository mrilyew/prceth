from representations.Representation import Representation
from resources.Descriptions import descriptions
from utils.MainUtils import parse_json

class Json(Representation):
    category = "Data"

    def declare():
        params = {}
        params["object"] = {
            "docs": {
                "definition": descriptions.get('__json_object_given_from_code')
            },
            "type": "object",
        }
        params["text"] = {
            "docs": {
                "definition": descriptions.get('__json_text_given_from_code')
            },
            "type": "text",
        }

        return params

    async def extractByText(self, i = {}):
        json_text = i.get('text')
        __obj = parse_json(json_text)

        out = self.new_cu({
            "source": {
                'type': 'api',
                'content': 'json',
            },
            'content': __obj,
        })

        return [out]

    async def extractByObject(self, i = {}):
        json_object = i.get('object')
        out = self.new_cu({
            "source": {
                'type': 'api',
                'content': 'json',
            },
            'content': json_object,
        })

        return [out]

    def extractWheel(self, i = {}):
        if 'object' in i:
            return 'extractByObject'
        elif 'text' in i:
            return 'extractByText'
