from executables.representations import Representation

keys = {
    "name": {
        "ru_RU": "Файл",
        "en_US": "File"
    },
    "definition": {
        "ru_RU": "Файл по пути на диске или URL",
        "en_US": "File by filepath or URL",
    },
}

class Implementation(Representation):
    docs = {
        "name": Representation.resolve_key(keys.get("name")),
        "definition": Representation.resolve_key(keys.get("definition")),
    }

    async def process_item(self, item):
        return item

    async def metadata(self, i = {}):
        return []
