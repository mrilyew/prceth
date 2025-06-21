from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from db.Models.Content.ContentUnit import ContentUnit
from peewee import fn
from declarable.ArgumentsTypes import IntArgument, BooleanArgument

class RandomContent(BaseAct):
    category = 'Random'

    @classmethod
    def declare(cls):
        params = {}
        params["limit"] = IntArgument({
            "default": 10,
            "assertion": {
                "not_null": True,
            },
        })
        params["raw_models"] = BooleanArgument({
            "default": False,
            "assertion": {
                "not_null": True,
            },
        })
        params["from_id"] = IntArgument({
            "default": None,
        })

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
