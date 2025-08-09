from executables.acts import BaseAct
from declarable.ArgumentsTypes import IntArgument, FloatArgument, StringArgument, LimitedArgument, BooleanArgument
from db.Models.Content.StorageUnit import StorageUnit
from functools import reduce
import operator

class Search(BaseAct):
    category = 'StorageUnits'

    @classmethod
    def declare(cls):
        params = {}
        params["query"] = StringArgument({
            "default": None,
        })
        params["order"] = LimitedArgument({
            "docs": {
                "name": "c.search.order.name",
                "values": {
                    "created_asc": {
                        "name": "c.search.order.c_asc.name",
                    },
                    "created_desc": {
                        "name": "c.search.order.c_desc.name"
                    },
                }
            },
            'values': ['created_asc', 'created_desc'],
            'default': 'created_desc',
        })
        params["count"] = IntArgument({
            "docs": {
                "name": "c.search.count.name",
            },
            "default": 100,
            "assertion": {
                "not_null": True,
            }
        })
        params["offset"] = IntArgument({
            "docs": {
                "name": "c.search.offset.name",
            },
        })

        return params

    async def execute(self, i = {}):
        count = i.get("count")
        order = i.get("order")
        offset = i.get("offset")
        query = i.get("query")

        assert count > 0, "count can't be negative"

        if offset != None:
            assert offset > 0, "offset can't be negative"

        select_query = StorageUnit.select()

        # direct search !
        if query != None:
            conditions = []
            columns = ["upload_name", "metadata"]

            for column in columns:
                conditions.append(
                    (getattr(StorageUnit, column) ** f'%{query}%')
                )

            if conditions:
                select_query = select_query.where(reduce(operator.or_, conditions))

        items_count = select_query.count()

        # Orders

        match(order):
            case 'created_desc':
                if offset != None:
                    select_query = select_query.where(StorageUnit.uuid < int(offset))

                select_query = select_query.order_by(StorageUnit.created_at.desc())
            case 'created_asc':
                if offset != None:
                    select_query = select_query.where(StorageUnit.uuid > int(offset))

                select_query = select_query.order_by(StorageUnit.created_at.asc())

        if count != None:
            select_query = select_query.limit(count)

        fnl = []

        for item in select_query:
            fnl.append(item.api_structure())

        return {
            'total_count': items_count,
            'items': fnl
        }
