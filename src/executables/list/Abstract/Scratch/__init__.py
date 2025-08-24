from executables.representations import Representation

keys = {
    "scratch.name": {
        "en_US": "No content",
        "ru_RU": "Без содержимого"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("scratch.name"),
    }
    executable_cfg =  {
        'free_args': True
    }
