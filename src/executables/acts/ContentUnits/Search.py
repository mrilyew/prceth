from executables.acts import BaseAct
from declarable.ArgumentsTypes import IntArgument, FloatArgument, StringArgument, LimitedArgument, BooleanArgument
from db.Models.Content.ContentUnit import ContentUnit

class Search(BaseAct):
    category = 'ContentUnits'

    @classmethod
    def declare(cls):
        params = {}
        params["count"] = IntArgument({
            "default": 10,
            "assertion": {
                "not_null": True,
            }
        })
        params["offset"] = IntArgument({})
        params["return_unlisted"] = BooleanArgument({
            "default": False
        })
        params["representation"] = StringArgument({})
        params["order"] = LimitedArgument({
            'values': ['created_asc', 'created_desc'],
            'default': 'created_desc',
        })

        return params

    async def execute(self, i = {}):
        count = i.get('count')
        representation = i.get('representation')
        order = i.get('order')
        return_unlisted = i.get('return_unlisted')
        offset = i.get('offset')

        query = ContentUnit.select().where(ContentUnit.deleted == 0)
        if representation != None:
            query = query.where(ContentUnit.representation == representation)

        if return_unlisted == False:
            query = query.where(ContentUnit.unlisted == 0)

        items_count = query.count()

        # Orders

        match(order):
            case 'created_desc':
                query = query.order_by(ContentUnit.created_at.desc())
                if offset != None:
                    query = query.where(ContentUnit.uuid > int(offset))
            case 'created_asc':
                query = query.order_by(ContentUnit.created_at.asc())
                if offset != None:
                    query = query.where(ContentUnit.uuid < int(offset))

        if count != None:
            query = query.limit(count)
        print(offset)
        print(query.sql())
        fnl = []

        for item in query:
            fnl.append(item.api_structure())

        return {
            'total_count': items_count,
            'items': fnl
        }
