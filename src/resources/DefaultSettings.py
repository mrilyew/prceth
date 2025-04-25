DefaultSettings = {
    "ui.lang": {
        "type": "string",
        "default": 'en',
    },
    "ui.name": {
        "type": "string",
        "default": "Difault",
    },
    "web.useragent": {
        "type": "string",
        "default": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    },
    "web.host": {
        "type": "string",
        "default": "127.0.0.1",
    },
    "web.port": {
        "type": "int",
        "default": 7856,
    },
    "web.max_speed": {
        "type": "int",
        "default": 2000, # kbs
    },
    "flask.debug": {
        "type": "int",
        "default": 1,
    },
    "flask.frontend": {
        "type": "string",
        "default": "default",
    },
    "extractor.cache_assets": {
        "type": "int",
        "default": 0, # If 1, on NT you should run CMD with admin privelegies
    },
    "storage.path": {
        "type": "string",
        "default": "?cwd?\\storage" # /src -> /storage
    },
    "db.path": {
        "type": "string",
        "default_value": "storage/dbs/main.db"
    },
    "net.timeout": {
        "type": "int",
        "default": 1000
    },
    "logger.skip_categories": {
        "type": "object",
        "default": []
    },
    # Thumbnails
    "thumbnail.width": {
        "type": "int",
        "default": 200,
    },
    "thumbnail.height": {
        "type": "int",
        "default": 200,
    },
}
