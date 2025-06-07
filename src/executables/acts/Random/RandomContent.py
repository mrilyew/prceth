from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from db.ContentUnit import ContentUnit
from peewee import fn

class RandomContent(BaseAct):
    category = 'Random'

    def declare():
        params = {}
        params["limit"] = {
            "type": "int",
            "default": 10,
            "docs": {
                "definition": descriptions.get('__limit_of_recieved_data')
            },
            "assertion": {
                "not_null": True,
            },
        }
        params["raw_models"] = {
            "type": "bool",
            "docs": {
                "definition": descriptions.get('__raw_model_explanation')
            },
            "default": False,
            "assertion": {
                "not_null": True,
            },
        }
        params["from_id"] = {
            "type": "int",
            "docs": {
                "definition": descriptions.get('__randomization_su_id')
            },
            "default": None,
        }

        return params

    async def execute(self, i = {}):
        self.args = i

        return {"items": await self._returnItems()}

    async def _returnItems(self):
        items = await self._recieveItems()
        fnl = []
        for item in items:
            if self.args.get("raw_models") == True:
                fnl.append(item)
            else:
                fnl.append(item.api_structure())

        return fnl

    async def _recieveItems(self):
        __ = None
        if self.args.get("from_id") == None:
            __ = ContentUnit.select().where(ContentUnit.deleted == 0).order_by(fn.Random()).limit(self.args.get('limit'))
        else:
            _col = ContentUnit.get(self.args.get("from_id"))
            assert _col != None, 'content_unit with this id does not exists'

            __ = ContentUnit.select().where(ContentUnit.id << _col._linksSelectionIds()).limit(self.args.get('limit')).order_by(fn.Random())

        return __
