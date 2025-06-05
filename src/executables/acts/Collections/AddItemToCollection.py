from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.ContentUnit import ContentUnit
from db.Collection import Collection

class AddItemToCollection(BaseAct):
    name = 'AddItemToCollection'
    category = 'Collections'
    docs = {
        "description": {
            "name": {
                "ru": "Добавить записи в коллекцию",
                "en": "Add entities to collection"
            },
            "definition": {
                "ru": "Добавляет записи в коллекцию по id",
                "en": "Adds entities to collection by id"
            },
        },
        "returns": {
            "end": True,
            "type": "int",
        }
    }

    def declare():
        params = {}
        params["collection_id"] = {
            "type": "int",
            "assertion": {
                "not_null": True,
            },
        }
        params["ContentUnit_id"] = {
            "type": "int",
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        collection_id = self.passed_params.get("collection_id")
        ContentUnit_id = self.passed_params.get("ContentUnit_id")

        assert collection_id != None and ContentUnit_id != None, "collection_id and ContentUnit_id are not passed"

        collection = Collection.get(collection_id)
        ContentUnit = ContentUnit.get(ContentUnit_id)

        assert collection != None, "collection not found"
        assert ContentUnit != None, "ContentUnit not found"

        collection.addItem(ContentUnit)

        return {
            "success": 1
        }
