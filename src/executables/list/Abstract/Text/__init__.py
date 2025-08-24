from executables.representations import Representation

keys = {
    "text.name": {
        "en_US": "Text",
        "ru_RU": "Текст"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("text.name"),
    }
