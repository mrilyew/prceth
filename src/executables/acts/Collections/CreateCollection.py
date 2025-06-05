from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from db.ContentUnit import ContentUnit

class CreateCollection(BaseAct):
    name = 'CreateCollection'
    category = 'Collections'
    docs = {
        "description": {
            "name": {
                "ru": "Создать коллекцию",
                "en": "Create collection"
            },
            "definition": {
                "ru": "Создаёт новую пустую коллекцию",
                "en": "Creates new empty collection"
            },
        },
        "returns": {
            "end": True,
            "type": "int",
        }
    }

    def declare():
        params = {}
        params["preview_id"] = {
            "type": "int",
            "default": None,
        }
        params["name"] = {
            "type": "string",
            "default": None,
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        preview_ContentUnit = None
        add_after = None
        collection_name = self.passed_params.get("name")

        assert len(collection_name) > 0, "name is too short"

        if "preview_id" in self.passed_params:
            __preview_ContentUnit = ContentUnit.get(int(self.passed_params.get("preview_id")))
            if __preview_ContentUnit != None:
                preview_ContentUnit = __preview_ContentUnit

        if "to_add" in self.passed_params:
            __add_collection = Collection.get(int(self.passed_params.get("to_add")))
            if __add_collection != None:
                add_after = __add_collection

        col = Collection()
        col.name = self.passed_params.get("name")
        col.description = self.passed_params.get("description")
        col.tags = self.passed_params.get("tags")
        if self.passed_params.get('frontend_data') != None:
            col.frontend_data = self.passed_params.get('frontend_data')

        if preview_ContentUnit != None:
            col.preview_id = preview_ContentUnit.id

        col.order = Collection.getAllCount()
        if add_after != None:
            col.unlisted = 1

        col.save(force_insert=True)
        if add_after != None:
            add_after.addItem(col)

        return col.getApiStructure()
