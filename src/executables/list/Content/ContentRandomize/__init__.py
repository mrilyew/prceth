from executables.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from db.LinkManager import LinkManager
from declarable.Arguments import IntArgument, BooleanArgument
from peewee import fn

class Implementation(Act):
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
        return {"items": await self._returnItems(i)}

    async def _returnItems(self, i):
        items = await self._recieveItems(i)
        fnl = []
        for item in items:
            if i.get("raw_models") == True:
                fnl.append(item)
            else:
                fnl.append(item.api_structure())

        return fnl

    async def _recieveItems(self, i):
        __ = None
        if i.get("from_id") == None:
            __ = ContentUnit.select().where(ContentUnit.is_unlisted == 0).order_by(fn.Random()).limit(i.get('limit'))
        else:

            _col = ContentUnit.get(i.get("from_id"))
            link_manager = LinkManager(_col)
            assert _col != None, 'content_unit with this id does not exists'

            __ = ContentUnit.select().where(ContentUnit.uuid.in_(link_manager.linksListId())).limit(i.get('limit')).order_by(fn.Random())

        return __
