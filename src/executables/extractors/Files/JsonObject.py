from executables.extractors.Base import BaseExtractor

class JsonObject(BaseExtractor):
    name = 'JsonObject'
    category = 'Files'
    hidden = True
    params = {
        "json_object": {
            "desc_key": "passed_json_object",
            "type": "object",
            "assert": True,
        }
    }
    
    def setArgs(self, args):
        self.passed_params["json_object"] = args.get("json_object")

        super().setArgs(args)

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
