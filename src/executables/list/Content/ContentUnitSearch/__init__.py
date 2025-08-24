from executables.acts import Act
from declarable.Arguments import IntArgument, CsvArgument, ContentUnitArgument, StringArgument, LimitedArgument, BooleanArgument
from db.Models.Content.ContentUnit import ContentUnit
from functools import reduce
from peewee import fn
import operator

keys = {
    "order.name": {
        "en_US": "Order",
        "ru_RU": "Порядок"
    }
}

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["query"] = StringArgument({
            "default": None,
        })
        params["representation"] = StringArgument({
            "docs": {
                "name": keys.get("order.name"),
            }
        })
        params["order"] = LimitedArgument({
            "docs": {
                "name": keys.get("order.name"),
                "values": {
                    "created_asc": {
                        "name": {
                            "en_US": "ID ↑"
                        },
                    },
                    "created_desc": {
                        "name": {
                            "en_US": "ID ↓"
                        }
                    },
                }
            },
            'values': ['created_asc', 'created_desc'],
            'default': 'created_desc',
        })
        params["count"] = IntArgument({
            "default": 100,
            "assertion": {
                "not_null": True,
            }
        })
        params["offset"] = IntArgument({})
        params["return_unlisted"] = BooleanArgument({
            "default": False,
        })
        params["collections_only"] = BooleanArgument({
            "default": False,
        })
        params["link"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "default": None,
        })
        params["ids"] = CsvArgument({
            "orig": IntArgument({}),
        })

        return params

    async def execute(self, i = {}):
        count = i.get("count")
        representation = i.get("representation")
        order = i.get("order")
        return_unlisted = i.get("return_unlisted")
        collections_only = i.get("collections_only")
        offset = i.get("offset")
        query = i.get("query")
        search_in = i.get("link")
        in_ids = i.get("ids")

        assert count > 0, "count can't be negative"

        if offset != None:
            assert offset > 0, "offset can't be negative"

        select_query = ContentUnit.select()
        if in_ids != None:
            select_query = select_query.where(ContentUnit.uuid.in_(in_ids))

        if representation != None:
            select_query = ContentUnit.json_search(select_query, ContentUnit.saved, "$.representation", representation)

        if return_unlisted == False:
            select_query = select_query.where(ContentUnit.is_unlisted == 0)

        if collections_only == True:
            select_query = select_query.where(ContentUnit.is_collection == 1)

        if search_in != None and len(search_in) > 0:
            _ids = []

            for item in search_in:
                if item:
                    _linked = item.linked_list

                    for _link in _linked:
                        if _link.short_name == "cu":
                            _ids.append(_link.uuid)

            assert len(_ids) > 0, "there is no linked"

            select_query = select_query.where(ContentUnit.uuid.in_(_ids))

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
