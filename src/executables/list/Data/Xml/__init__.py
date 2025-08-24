from executables.representations import Representation
from declarable.Arguments import StringArgument, ObjectArgument
import xmltodict

keys = {
    "xml.name": {
        "en_US": "Xml"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("xml.name"),
    }

    class Extractor(Representation.ExtractStrategy):
        async def extractByText(self, i = {}):
            xml_text = i.get('text')

            out = self.ContentUnit()
            out.content = xmltodict.parse(xml_text)

            return [out]
 
        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByText'
