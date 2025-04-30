from executables.extractors.Base.Base import BaseExtractor
from resources.Globals import Path, file_manager, utils, json
from resources.Exceptions import InvalidPassedParam, NotPassedException
from db.File import File

class Scratch(BaseExtractor):
    name = 'Scratch'
    category = 'Files'

    def declare():
        params = {}
        params["suggested_name"] = {
            "desc_key": "-",
            "type": "string",
        }
        params["declared_created_at"] = {
            "desc_key": "-",
            "type": "int",
            "default": 1234,
        }
        params["internal_content"] = {
            "desc_key": "-",
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
