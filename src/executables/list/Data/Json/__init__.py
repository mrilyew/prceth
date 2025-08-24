from executables.representations import Representation

keys = {
    "json.name": {
        "en_US": "JSON"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("json.name"),
    }
