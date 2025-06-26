from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument
from db.DbInsert import db_insert

class Hyperlink(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["url"] = StringArgument({
            "default": None,
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        def extractWheel(self, i = {}):
            if 'url' in i:
                return 'extractByUrl'

        async def extractByUrl(self, i = {}):
            url = i.get('url')

            # TODO add opengraph parse
            out = db_insert.contentFromJson({
                'content': {
                    "url": str(url),
                },
            })

            return [out]
