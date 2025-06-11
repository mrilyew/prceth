from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection
from repositories.RepresentationsRepository import RepresentationsRepository
from declarable.ArgumentsTypes import StringArgument

class MethodsList(BaseAct):
    name = 'MethodsList'
    category = 'Representations'
    docs = {
        "name": {
            "ru": ":)",
            "en": ":)"
        },
        "definition": {
            "ru": ":)",
            "en": ":)"
        }
    }

    def declare():
        params = {}
        params["representation"] = StringArgument({
            "default": None,
            "docs": {
                "definition": {}
            },
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, args = {}):
        __repr = RepresentationsRepository().getByName(args.get('representation'))

        return {
            "methods": __repr.rawListMethods()
        }
