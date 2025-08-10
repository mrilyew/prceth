from executables.representations import Representation
from declarable.ArgumentsTypes import StringArgument
from db.DbInsert import db_insert

class Collection(Representation):
    docs = {
        "name": "representations.abstract.collection.name",
        "definition": "representations.abstract.collection.definition",
    }
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["name"] = StringArgument({
            'docs': {
                "name": 'abstract_collection_name_param_title',
                "definition": 'abstract_collection_name_param_description',
            },
            'assertion': {
                'not_null': True
            }
        })
        params["description"] = StringArgument({
            'is_long': True,
            'docs': {
                "name": 'abstract_collection_description_param_title',
                "definition": 'abstract_collection_description_param_description',
            },
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        async def extractByDefault(self, i = {}):
            out = db_insert.contentFromJson({
                'content': {},
                'display_name': i.get('name'),
                'description': i.get('description'),
                'is_collection': True,
            })

            return [out]

        def extractWheel(self, i = {}):
            return 'extractByDefault'
