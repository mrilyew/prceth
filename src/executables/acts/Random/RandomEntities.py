from executables.acts.Base.BaseRandomizator import BaseRandomizator
from db.Collection import Collection
from db.ContentUnit import ContentUnit
from peewee import fn

class RandomEntities(BaseRandomizator):
    name = 'RandomEntities'
    category = 'random'
    docs = {
        "description": {
            "name": {
                "ru": "Случайные записи",
                "en": "Random entities"
            },
            "definition": {
                "ru": "Возвращает случайные записи на основе параметров",
                "en": "Returns random entities from params"
            }
        }
    }

    def declare():
        params = {}
        params["raw_models"] = {
            "type": "bool",
            "docs": {
                "definition": {
                    "ru": "Возвращать модели в виде экземпляров класса (1) либо в виде api-представления (0)",
                    "en": "Return models as class instances (1) or json object (0)",
                }
            },
            "default": False,
            "assertion": {
                "not_null": True,
            },
        }
        params["collection_id"] = {
            "type": "int",
            "docs": {
                "definition": {
                    "ru": "ID коллекции, в которой проводить рандомизацию",
                    "en": "Randomization collection ID",
                }
            },
            "default": None,
        }

        return params

    async def _returnItems(self):
        entities = await self._recieveItems()
        fnl = []
        for ContentUnit in entities:
            if self.passed_params.get("raw_models") == True:
                fnl.append(ContentUnit)
            else:
                fnl.append(ContentUnit.getApiStructure())

        return fnl

    async def _recieveItems(self):
        __ = None
        if self.passed_params.get("collection_id") == None:
            __ = ContentUnit.fetchItems().order_by(fn.Random()).limit(self.passed_params.get('limit'))
        else:
            _col = Collection.get(self.passed_params.get("collection_id"))
            assert _col != None, 'invalid collection_id'

            __ = _col.getItems(limit=self.passed_params.get('limit'),order="rand")

        return __
