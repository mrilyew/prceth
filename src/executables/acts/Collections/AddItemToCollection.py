from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Entity import Entity
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
                "assert_not_null": True,
            },
        }
        params["entity_id"] = {
            "type": "int",
            "assertion": {
                "assert_not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        collection_id = self.passed_params.get("collection_id")
        entity_id = self.passed_params.get("entity_id")

        assert collection_id != None and entity_id != None, "collection_id and entity_id are not passed"

        collection = Collection.get(collection_id)
        entity = Entity.get(entity_id)

        assert collection != None, "collection not found"
        assert entity != None, "entity not found"

        collection.addItem(entity)

        return {
            "success": 1
        }
