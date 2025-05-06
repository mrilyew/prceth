from executables.extractors.Base.Base import BaseExtractor

class JsonObject(BaseExtractor):
    name = 'JsonObject'
    category = 'Files'
    hidden = True
    docs = {
        "description": {
            "name": {
                "ru": "JSON объект",
                "en": "JSON object"
            },
            "definition": {
                "ru": "Создаёт запись из JSON",
                "en": "Creates entity from JSON"
            }
        }
    }

    def declare(self, args):
        params = {}
        params["json_object"] = {
            "docs": {
                "definition": {
                    "ru": "JSON объект, переданный из кода",
                    "en": "JSON object",
                }
            },
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
