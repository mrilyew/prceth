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
        "name": keys.get("name"),
        "definition": keys.get("definition"),
    }

    @staticmethod
    async def process_item(item):
        return item

    async def metadata(self, i = {}):
        return []
