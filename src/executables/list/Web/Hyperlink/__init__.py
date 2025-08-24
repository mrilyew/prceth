from executables.representations import Representation

keys = {
    "hyperlink.name": {
        "en_US": "Hyperlink",
        "ru_RU": "Ссылка"
    },
    "hyperlink.definition": {
        "en_US": "Hyperlink to web-site",
        "ru_RU": "Ссылка на web-ресурс"
    }
}

class Implementation(Representation):
    docs = {
        "definition": keys.get("hyperlink.definition"),
        "name": keys.get("hyperlink.name"),
    }
