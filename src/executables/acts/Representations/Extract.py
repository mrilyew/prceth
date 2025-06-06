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
        representationClass = RepresentationsRepository().getByName(i.get('representation'))
        __ents = await representationClass().safeExtract(i)
        __all_items = []

        for item in __ents:
            item.save()

            __item = item.api_structure()
            __all_items.append(__item)

        return {
            "items": __all_items
        }
