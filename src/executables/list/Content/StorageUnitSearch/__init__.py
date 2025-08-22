from executables.acts import Act
from declarable.Arguments import ContentUnitArgument, IntArgument, CsvArgument, StringArgument, LimitedArgument, BooleanArgument
from db.Models.Content.StorageUnit import StorageUnit
from functools import reduce
import operator

class Implementation(Act):
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
        params["return_thumbnails"] = BooleanArgument({
            "default": False,
            "docs": {
                "name": "c.search.return_thumbnails.name",
            },
        })
        params["link"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "default": None,
            "docs": {
                "name": "c.search.link.name",
            },
        })

        return params

    async def execute(self, i = {}):
        count = i.get("count")
        order = i.get("order")
        offset = i.get("offset")
        query = i.get("query")
        return_thumbnails = i.get("return_thumbnails")
        search_in = i.get("link")

        assert count > 0, "count can't be negative"

        if offset != None:
            assert offset > 0, "offset can't be negative"

        select_query = StorageUnit.select()

        if return_thumbnails == False:
            select_query = select_query.where(StorageUnit.is_thumbnail == 0)

        if query != None:
            conditions = []
            columns = ["upload_name", "metadata"]

            for column in columns:
                conditions.append(
                    (getattr(StorageUnit, column) ** f'%{query}%')
                )

            if conditions:
                select_query = select_query.where(reduce(operator.or_, conditions))

        if search_in != None and len(search_in) > 0:
            _ids = []

            for item in search_in:
                if item:
                    _linked = item.linked_list

                    for _link in _linked:
                        if _link.short_name == "su":
                            _ids.append(_link.uuid)

            assert len(_ids) > 0, "invalid links"

            select_query = select_query.where(ContentUnit.uuid.in_(_ids))

        items_count = select_query.count()

        # Orders

        match(order):
            case 'created_desc':
                if offset != None:
                    select_query = select_query.where(StorageUnit.uuid < int(offset))

                select_query = select_query.order_by(StorageUnit.uuid.desc())
            case 'created_asc':
                if offset != None:
                    select_query = select_query.where(StorageUnit.uuid > int(offset))

                select_query = select_query.order_by(StorageUnit.uuid.asc())

        if count != None:
            select_query = select_query.limit(count)

        fnl = []

        for item in select_query:
            fnl.append(item.api_structure())

        return {
            'total_count': items_count,
            'items': fnl
        }
