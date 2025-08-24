from executables.representations import Representation

keys = {
    "collection.name": {
        "en_US": "Collection",
        "ru_RU": "Коллекция"
    },
}

class Implementation(Representation):
    docs = {
        "name": keys.get("collection.name"),
    }
    executable_cfg = {
        'free_args': True
    }
