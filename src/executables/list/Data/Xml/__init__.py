from executables.representations import Representation
from declarable.Arguments import StringArgument, ObjectArgument
import xmltodict

class Implementation(Representation):
    docs = {
        "name": "representations.data.xml.name",
    }

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({})

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByText(self, i = {}):
            xml_text = i.get('text')

            out = self.ContentUnit()
            out.content = xmltodict.parse(xml_text)

            return [out]
 
        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByText'
