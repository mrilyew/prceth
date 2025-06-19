from representations.Representation import Representation
from representations.ExtractStrategy import ExtractStrategy
from declarable.ArgumentsTypes import StringArgument, LimitedArgument, CsvArgument
from db.Content.ContentUnit import ContentUnit

class Collection(Representation):
    category = "Abstract"
    executable_cfg =  {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["name"] = StringArgument({
            'assertion': {
                'not_null': True
            }
        })
        params["description"] = StringArgument({})

        return params

    class Extractor(ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = self.contentUnit({
                'content': {},
                'display_name': i.get('name'),
                'description': i.get('description'),
                'is_collection': True,
            })

            return [out]

        def extractWheel(self, i = {}):
            return 'extractByDefault'
