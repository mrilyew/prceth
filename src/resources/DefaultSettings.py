DefaultSettings = {
    "ui.lang": {
        "type": "string",
        "default": 'en',
    },
    "ui.name": {
        "type": "string",
        "default": "Prethmeta",
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
        "default": 7782,
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
    "storage.root_path": {
        "type": "string",
        "default": "?cwd?/storage" # cwd -> /storage
    },
    "db.sqlite_content_path": {
        "type": "string",
        "default": "?cwd?/storage/dbs/content.db"
    },
    "db.sqlite_instance_path": {
        "type": "string",
        "default": "?cwd?/storage/dbs/instance.db"
    },
    "net.timeout": {
        "type": "int",
        "default": 100
    },
    "logger.skip_categories": {
        "type": "object",
        "default": []
    },
    "logger.skip_file": {
        "type": "int",
        "default": 0,
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
