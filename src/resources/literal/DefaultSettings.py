DefaultSettings = {
    "ui.lang": {
        "type": "string",
        "default_value": 'ru',
    },
    "ui.name": {
        "type": "string",
        "default_value": "LCM/S",
    },
    "net.useragent": {
        "type": "string",
        "default_value": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    },
    "net.host": {
        "type": "string",
        "default_value": "127.0.0.1",
    },
    "net.port": {
        "type": "int",
        "default_value": 5667,
    },
    "flask.debug": {
        "type": "int",
        "default_value": 1,
    },
    "extractor.cache_assets": {
        "type": "int",
        "default_value": 0, # If 1, on windows you should run CMD with admin privelegies
    },
    "storage.path": {
        "type": "string",
        "default_value": "?cwd?/storage" # /src -> /storage
    },
}
