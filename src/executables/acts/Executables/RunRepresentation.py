from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection
from repositories.RepresentationsRepository import RepresentationsRepository
from declarable.ArgumentsTypes import StringArgument

class RunRepresentation(BaseAct):
    category = 'Representations'
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["representation"] = StringArgument({
            "default": None,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        representationClass = RepresentationsRepository().getByName(i.get('representation'))
        assert representationClass.canBeExecuted() == True, "representation cannot be executed"

        __ents = await representationClass.extract(i)
        __all_items = []

        for item in __ents:
            item.save()

            __item = item.api_structure()
            __all_items.append(__item)

        return {
            "items": __all_items
        }
