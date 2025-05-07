from executables.extractors.Base.Base import BaseExtractor
from resources.Globals import json

class Scratch(BaseExtractor):
    name = 'Scratch'
    category = 'Files'
    docs = {
        "description": {
            "name": {
                "ru": "Пустота",
                "en": "Scratch"
            },
            "definition": {
                "ru": "Запись из ничего",
                "en": "Entity from scratch"
            }
        }
    }

    def declare():
        params = {}
        params["suggested_name"] = {
            "docs": {
                "definition": {
                    "ru": "Название",
                    "en": "Name",
                }
            },
            "type": "string",
        }
        params["declared_created_at"] = {
            "docs": {
                "definition": {
                    "ru": "Возможная дата создания",
                    "en": "Declared creation date",
                }
            },
            "type": "int",
            "default": 1234,
        }
        params["internal_content"] = {
            "docs": {
                "definition": {
                    "ru": "JSON контент",
                    "en": "JSON content",
                }
            },
            "type": "string",
            "default": "{}",
        }

        return params

    async def run(self, args):
        ENTITY = self._entityFromJson({
            "source": "api:null",
            "suggested_name": self.passed_params.get("suggested_name"),
            "declared_created_at": int(self.passed_params.get("declared_created_at")),
            "internal_content": json.loads(self.passed_params.get("internal_content")),
        })

        return {
            "entities": [ENTITY],
        }
