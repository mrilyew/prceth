from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection
from repositories.RepresentationsRepository import RepresentationsRepository

class Extract(BaseAct):
    name = 'Extract'
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
    declaration_cfg = {
        'free_args': True
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

    async def execute(self, i = {}):
        __repr = RepresentationsRepository().getByName(i.get('representation'))
        await __repr().safeExtract(i)

        return {
            "res": 1
        }
