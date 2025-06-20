from representations.Representation import Representation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from representations.ExtractStrategy import ExtractStrategy
from db.DbInsert import db_insert
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

            out = db_insert.contentFromJson({
                'content': xmltodict.parse(xml_text),
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByText'
