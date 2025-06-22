from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument, ObjectArgument
from db.DbInsert import db_insert
import xmltodict

class Xml(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({})
        params["json"] = ObjectArgument({})

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByText(self, i = {}):
            xml_text = i.get('text')

            out = db_insert.contentFromJson({
                'content': xmltodict.parse(xml_text),
            })

            return [out]

        def extractWheel(self, i = {}):
            if 'text' in i:
                return 'extractByText'
