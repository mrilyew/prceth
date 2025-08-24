from executables.representations import Representation
from declarable.Arguments import StringArgument

class Method(Representation.AbstractExtractor):
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

    async def execute(self, i = {}):
        out = self.ContentUnit()
        out.content = {}
        out.display_name = i.get('name')
        out.description = i.get('description')
        out.is_collection = True

        return [out]
