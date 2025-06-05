from executables.acts.Export.ExportContentUnit import ExportContentUnit
from db.Collection import Collection

class ExportCollection(ExportContentUnit):
    name = 'ExportCollection'
    category = 'export'
    docs = {
        "description": {
            "name": {
                "ru": "Экспорт коллекции",
                "en": "Collection export"
            },
            "definition": {
                "ru": "Копирует записи из коллекции в переданную директорию",
                "en": "Copies entities from collection to provided directory"
            },
        },
        "returns": {
            "destination": {
                "end": True,
                "type": "string",
                "explanation": {
                    "ru": "Папка, в которую были сохранены файлы",
                    "en": "Folder where files was saved",
                }
            }
        }
    }

    main_args = {
        "list": ["dir", "ids"],
        "type": "and",
        "ignore": ["ids"]
    }

    def declare():
        params = {}
        params["collection_id"] = {
            "type": "int",
            "assertion": {
                "not_null": True,
            },
        }
        params["ids"] = None

        return params

    async def execute(self, args = {}):
        _i_entities_ids = self.passed_params.get("collection_id")

        collection_ids = str(_i_entities_ids).split(",")
        entities = []
        ContentUnit_ids = []
        collections = []
        for coll_id in collection_ids:
            collections.append(Collection.get(int(coll_id)))

        assert len(collections) > 0, "no collections found"

        for coll in collections:
            for __ContentUnit in coll.getItems(limit=None):
                if __ContentUnit.self_name == "collection": # TODO
                    continue
                entities.append(__ContentUnit)
        for __ContentUnit in entities:
            ContentUnit_ids.append(str(__ContentUnit.id))

        fs_act = ExportContentUnit()
        fs_act.setArgs(self.passed_params.update({
            "ids": ",".join(ContentUnit_ids)
        }))

        export_res = await fs_act.execute()

        DESTINATION_DIR = export_res.get("destination")
        for coll in collections:
            coll.saveInfoToJson(dir=DESTINATION_DIR)

        return {
            "destination": DESTINATION_DIR
        }
