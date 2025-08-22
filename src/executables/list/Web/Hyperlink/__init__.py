from executables.representations import Representation
from declarable.Arguments import CsvArgument

class Implementation(Representation):
    docs = {
        "definition": "representations.data.hyperlink.definition",
        "name": "representations.data.hyperlink.name",
    }

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
                out = self.ContentUnit()
                out.content = {
                    'url': str(url),
                }
                # TODO add opengraph parse

                outs.append(out)

            return outs
