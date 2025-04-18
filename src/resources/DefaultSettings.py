DefaultSettings = {
    "ui.lang": {
        "type": "string",
        "default_value": 'en',
    },
    "ui.name": {
        "type": "string",
        "default_value": "Difault",
    },
    "web.useragent": {
        "type": "string",
        "default_value": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    },
    "web.host": {
        "type": "string",
        "default_value": "127.0.0.1",
    },
    "web.port": {
        "type": "int",
        "default_value": 7856,
    },
    "flask.debug": {
        "type": "int",
        "default_value": 1,
    },
    "flask.frontend": {
        "type": "string",
        "default_value": "default",
    },
    "extractor.cache_assets": {
        "type": "int",
        "default_value": 0, # If 1, on NT you should run CMD with admin privelegies
    },
    "storage.path": {
        "type": "string",
        "default_value": "?cwd?\\storage" # /src -> /storage
    },
    "db.path": {
        "type": "string",
        "default_value": "storage/dbs/main.db"
    }
}
