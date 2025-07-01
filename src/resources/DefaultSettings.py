from declarable.ArgumentsTypes import StringArgument, IntArgument, BooleanArgument, LimitedArgument, ObjectArgument

DefaultSettings = {
    "ui.lang": StringArgument({
        "default": 'eng',
    }),
    "ui.name": StringArgument({
        "default": "Preth",
    }),
    "web.useragent": StringArgument({
        "default": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    }),
    "web.host": StringArgument({
        "default": "127.0.0.1",
    }),
    "web.port": IntArgument({
        "default": 26666,
    }),
    "web.max_speed": IntArgument({
        "default": 2000, # kbs
    }),
    "web.debug": BooleanArgument({
        "default": True,
    }),
    "storage.root_path": StringArgument({
        "default": "?cwd?/storage" # cwd -> /storage
    }),
    "db.content_db.type": LimitedArgument({
        "values": ['sqlite', 'mysql', 'postgresql'],
        "default": "sqlite",
    }),
    "db.instance_db.type": LimitedArgument({
        "values": ['sqlite', 'mysql', 'postgresql'],
        "default": "sqlite",
    }),
    "db.sqlite.content_db.name": StringArgument({
        "default": "?cwd?/storage/dbs/content.db"
    }),
    "db.sqlite.instance_db.name": StringArgument({
        "default": "?cwd?/storage/dbs/instance.db"
    }),
    "db.server_db.content_db.name": StringArgument({
        "default": "th_content"
    }),
    "db.server_db.instance_db.name": StringArgument({
        "default": "th_instance"
    }),
    "db.server_db.user": StringArgument({
        "default": None,
    }),
    "db.server_db.password": StringArgument({
        "default": None,
    }),
    "db.server_db.host": StringArgument({
        "default": '127.0.0.1',
    }),
    "db.server_db.port": IntArgument({
        "default": 3306,
    }),
    "net.timeout": IntArgument({
        "default": 100
    }),
    "logger.skip_categories": ObjectArgument({
        "default": []
    }),
    "logger.skip_file": BooleanArgument({
        "default": 0,
    }),
    # Thumbnails
    "thumbnail.width": IntArgument({
        "default": 200,
    }),
    "thumbnail.height": IntArgument({
        "default": 200,
    }),
}
