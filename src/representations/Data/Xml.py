from representations.Representation import Representation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from representations.ExtractStrategy import ExtractStrategy
import xmltodict

class Xml(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({
            "docs": {
                "definition": '__xml_text_pass'
            },
        })
        params["json"] = ObjectArgument({
            "docs": {
                "definition": '__xml_already_parsed'
            },
        })

        return params

    class Extractor(ExtractStrategy):
        async def extractByText(self, i = {}):
            xml_text = i.get('text')

            out = self.contentUnit({
                'content': xmltodict.parse(xml_text),
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByText'
