from executables.acts.Base.Base import BaseAct
from repositories.RepresentationsRepository import RepresentationsRepository
from declarable.ArgumentsTypes import StringArgument, CsvArgument
from db.DbFind import db_find

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
        params["link"] = CsvArgument({
            "default": []
        })

        return params

    async def execute(self, i = {}):
        representationClass = RepresentationsRepository().getByName(i.get('representation'))
        assert representationClass.canBeExecuted() == True, "representation cannot be executed"

        __ents = await representationClass.extract(i)
        __all_items = []
        __ids = i.get('link')
        __link_to = db_find.fromStringDifferentTypes(__ids)

        for item in __ents:
            item.save(force_insert=True)
            for _item in __link_to:
                item.addLink(_item)

            __item = item.api_structure()
            __all_items.append(__item)

        return {
            "items": __all_items
        }
