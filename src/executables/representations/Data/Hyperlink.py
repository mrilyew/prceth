from executables.representations import Representation
from declarable.ArgumentsTypes import CsvArgument
from db.DbInsert import db_insert

class Hyperlink(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["url"] = CsvArgument({
            "default": None,
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        def extractWheel(self, i = {}):
            if 'url' in i:
                return 'extractByUrl'

        async def extractByUrl(self, i = {}):
            urls = i.get('url')
            outs = []

            for url in urls:
                # TODO add opengraph parse
                out = db_insert.contentFromJson({
                    'content': {
                        "url": str(url),
                    },
                })

                outs.append(out)

            return outs
