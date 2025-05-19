from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json, often_params
from executables.acts.Base.Base import BaseAct
from db.Entity import Entity

class GetGlobalEntities(BaseAct):
    name = 'GetGlobalEntities'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}
        params["count"] = often_params.get("count_default_10")
        params["offset"] = often_params.get("offset_default_0")
        params["columns_search"] = {
            "type": "csv",
            "default": ['original_name', 'display_name'],
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["return_raw"] = often_params.get("return_raw")

        return params

    async def execute(self, args={}):
        columns_search = ['original_name', 'display_name']
        for column in ['description', 'source', 'index', 'saved', 'author']:
            if column in self.passed_params.get("columns_search"):
                columns_search.append(column)
        
        query = self.passed_params.get("query")
        if query == None:
            query = ""
        
        offset = self.passed_params.get("offset")
        count = self.passed_params.get("count")

        fetch = Entity.fetchItems(query=query,columns_search=columns_search)
        items = fetch.order_by(Entity.id.desc()).offset(offset).limit(count)
        final_items = []
        for item in items:
            final_items.append(item)

        count = fetch.count()

        return {"items": items, "count": count}
