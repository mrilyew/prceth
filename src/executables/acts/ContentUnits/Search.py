from executables.acts import BaseAct
from declarable.ArgumentsTypes import IntArgument, StringArgument, LimitedArgument
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
        params["timestamp_after"] = IntArgument({})
        params["representation"] = StringArgument({})
        params["order"] = LimitedArgument({
            'values': ['created_asc', 'created_desc'],
            'default': 'created_desc',
        })

        return params

    async def execute(self, i = {}):
        count = i.get('count')
        timestamp_after = i.get('timestamp_after')
        by_representation = i.get('representation')
        order = i.get('order')

        cnt = ContentUnit.select().where(ContentUnit.deleted == 0)
        items_count = cnt.count()

        if count != None:
            cnt = cnt.limit(count)

        if timestamp_after != None:
            cnt = cnt.where(ContentUnit.created_at > int(timestamp_after))

        if by_representation != None:
            cnt = cnt.where(ContentUnit.representation == by_representation)

        match(order):
            case 'created_desc':
                cnt = cnt.order_by(ContentUnit.created_at.desc())
            case 'created_asc':
                cnt = cnt.order_by(ContentUnit.created_at.asc())

        fnl = []

        for item in cnt:
            fnl.append(item.api_structure())

        return {
            'count': items_count,
            'items': fnl
        }
