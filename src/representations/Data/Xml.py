from representations.Representation import Representation
from resources.Descriptions import descriptions
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
import xmltodict

class Xml(Representation):
    category = "Data"

    def declare():
        params = {}
        params["text"] = StringArgument({
            "docs": {
                "definition": descriptions.get('__xml_text_pass')
            },
        })
        params["json"] = ObjectArgument({
            "docs": {
                "definition": descriptions.get('__xml_already_parsed')
            },
        })

        return params

    async def extractByText(self, i = {}):
        xml_text = i.get('text')

        out = self.new_cu({
            'content': xmltodict.parse(xml_text),
        })

        return [out]

    def extractWheel(self, i = {}):
        return 'extractByText'
