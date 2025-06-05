from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection
from repositories.RepresentationsRepository import RepresentationsRepository

class MethodsList(BaseAct):
    name = 'MethodsList'
    category = 'Representations'
    docs = {
        "description": {
            "name": {
                "ru": ":)",
                "en": ":)"
            },
            "definition": {
                "ru": ":)",
                "en": ":)"
            }
        }
    }

    def declare():
        params = {}
        params["representation"] = {
            "type": "string",
            "default": None,
            "docs": {
                "definition": {}
            },
            "assertion": {
                "not_null": True,
            }
        }

        return params

    async def execute(self, args={}):
        __repr = RepresentationsRepository().getByName(self.passed_params.get('representation'))

        return {
            "methods": __repr.rawListMethods()
        }
