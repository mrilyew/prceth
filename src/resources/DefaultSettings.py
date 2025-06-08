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
    "db.content_db.type": {
        "type": "array",
        "values": ['sqlite', 'mysql', 'postgresql'],
        "default": "sqlite",
    },
    "db.instance_db.type": {
        "type": "array",
        "values": ['sqlite', 'mysql', 'postgresql'],
        "default": "sqlite",
    },
    "db.sqlite.content_db.name": {
        "type": "string",
        "default": "?cwd?/storage/dbs/content.db"
    },
    "db.sqlite.instance_db.name": {
        "type": "string",
        "default": "?cwd?/storage/dbs/instance.db"
    },
    "db.server_db.content_db.name": {
        "type": "string",
        "default": "th_content"
    },
    "db.server_db.instance_db.name": {
        "type": "string",
        "default": "th_instance"
    },
    "db.server_db.user": {
        "type": "string",
        "default": None,
    },
    "db.server_db.password": {
        "type": "string",
        "default": None,
    },
    "db.server_db.host": {
        "type": "string",
        "default": '127.0.0.1',
    },
    "db.server_db.port": {
        "type": "int",
        "default": 3306,
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
