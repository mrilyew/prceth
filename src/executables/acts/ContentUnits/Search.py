from executables.acts import BaseAct
from declarable.ArgumentsTypes import IntArgument, FloatArgument, StringArgument, LimitedArgument, BooleanArgument
from db.Models.Content.ContentUnit import ContentUnit
from functools import reduce
import operator

class Search(BaseAct):
    @classmethod
    def declare(cls):
        params = {}
        params["query"] = StringArgument({
            "default": None,
        })
        params["representation"] = StringArgument({
            "docs": {
                "name": "c.search.representation.name",
            }
        })
        params["extractor"] = StringArgument({
            "docs": {
                "name": "c.search.extractor.name",
            }
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
        params["return_unlisted"] = BooleanArgument({
            "default": False,
            "docs": {
                "name": "c.search.return_unlisted.name",
            },
        })
        params["collections_only"] = BooleanArgument({
            "default": False,
            "docs": {
                "name": "c.search.collections_only.name",
            },
        })

        return params

    async def execute(self, i = {}):
        count = i.get("count")
        representation = i.get("representation")
        extractor = i.get("extractor")
        order = i.get("order")
        return_unlisted = i.get("return_unlisted")
        collections_only = i.get("collections_only")
        offset = i.get("offset")
        query = i.get("query")

        assert count > 0, "count can't be negative"

        if offset != None:
            assert offset > 0, "offset can't be negative"

        select_query = ContentUnit.select().where(ContentUnit.deleted == 0)
        if representation != None:
            select_query = select_query.where(ContentUnit.representation == representation)

        if extractor != None:
            select_query = select_query.where(ContentUnit.extractor == extractor)

        if return_unlisted == False:
            select_query = select_query.where(ContentUnit.unlisted == 0)

        if collections_only == True:
            select_query = select_query.where(ContentUnit.is_collection == 1)

        # direct search !
        if query != None:
            conditions = []
            columns = ["display_name", "description"]

            for column in columns:
                conditions.append(
                    (getattr(ContentUnit, column) ** f'%{query}%')
                )

            if conditions:
                select_query = select_query.where(reduce(operator.or_, conditions))

        items_count = select_query.count()

        # Orders

        match(order):
            case 'created_desc':
                if offset != None:
                    select_query = select_query.where(ContentUnit.uuid < int(offset))

                select_query = select_query.order_by(ContentUnit.created_at.desc())
            case 'created_asc':
                if offset != None:
                    select_query = select_query.where(ContentUnit.uuid > int(offset))

                select_query = select_query.order_by(ContentUnit.created_at.asc())

        if count != None:
            select_query = select_query.limit(count)

        fnl = []

        for item in select_query:
            fnl.append(item.api_structure())

        return {
            'total_count': items_count,
            'items': fnl
        }
