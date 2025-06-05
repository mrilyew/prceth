from resources.Globals import often_params
from executables.acts.Base.Base import BaseAct
from db.ContentUnit import ContentUnit

class Search(BaseAct):
    name = 'Search'
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
                "not_null": True,
            },
        }
        params["return_raw"] = often_params.get("return_raw")

        return params

    async def execute(self, args={}):
        columns_search = ['original_name', 'display_name']
        __return_raw = self.passed_params.get("return_raw")

        for column in ['description', 'source', 'internal_content', 'saved', 'author']:
            if column in self.passed_params.get("columns_search"):
                columns_search.append(column)
        
        query = self.passed_params.get("query")
        if query == None:
            query = ""
        
        offset = self.passed_params.get("offset")
        count = self.passed_params.get("count")

        fetch = ContentUnit.fetchItems(query=query,columns_search=columns_search)
        items = fetch.order_by(ContentUnit.id.desc()).offset(offset).limit(count)
        final_items = []
        for item in items:
            final_items.append(item)

        final_lists = []
        final_count = fetch.count()
        for item in items:
            if __return_raw == False:
                final_lists.append(item.getApiStructure())
            else:
                final_lists.append(item)

        return {"items": final_lists, "count": final_count}
