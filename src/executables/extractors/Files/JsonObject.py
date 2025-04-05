from executables.extractors.Base import BaseExtractor

class JsonObject(BaseExtractor):
    name = 'JsonObject'
    category = 'Files'
    hidden = True
    
    def declare(self, args):
        params = {}
        params["json_object"] = {
            "desc_key": "passed_json_object",
            "type": "object",
            "assert": {
                "assert_not_null": True,
            },
        }

        return params

    async def run(self, args):
        ENTITY = self._entityFromJson({
            "source": "api:json",
            "suggested_name": "file.json",
            "internal_content": self.passed_params.get("json_object"),
        })

        return {
            "entities": [
                ENTITY
            ],
        }
