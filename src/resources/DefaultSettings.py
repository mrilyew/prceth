from declarable.ArgumentsTypes import StringArgument, IntArgument, BooleanArgument, LimitedArgument, CsvArgument

DefaultSettings = {
    "ui.lang": StringArgument({
        "default": 'eng',
        "docs": {
            "name": "config.ui.lang.name",
        },
    }),
    "ui.name": StringArgument({
        "default": "Prceth",
        "docs": {
            "name": "config.ui.name.name",
        },
    }),
    "web.config_editing.allow": BooleanArgument({ # Allow to edit config from web
        "default": True,
    }),
    "web.env_editing.allow": BooleanArgument({ # Allow to edit env variables from web
        "default": False,
    }),
    "web.host": StringArgument({
        "default": "127.0.0.1",
        "docs": {
            "name": "config.web.host.name",
        },
    }),
    "web.port": IntArgument({
        "default": 26666,
        "docs": {
            "name": "config.web.port.name",
        },
    }),
    "web.debug": BooleanArgument({
        "default": True,
    }),
    "storage.root_path": StringArgument({
        "default": "?cwd?/storage", # cwd -> /storage
        "docs": {
            "name": "config.storage.root_path.name",
            "definition": "config.storage.root_path.definition",
        },
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
    "net.max_speed": IntArgument({
        "default": 2000, # kbs
        "docs": {
            "name": "config.net.max_speed.name",
            "definition": "config.net.max_speed.definition",
        },
    }),
    "net.useragent": StringArgument({
        "default": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        "docs": {
            "name": "config.net.useragent.name",
        },
    }),
    "net.timeout": IntArgument({
        "default": 100,
        "docs": {
            "name": "config.net.timeout.name",
            "definition": "config.net.timeout.definition",
        },
    }),
    "logger.skip_categories": CsvArgument({
        "default": [],
        "orig": StringArgument({}),
        "docs": {
            "name": "config.logger.skip_categories.name",
            "definition": "config.logger.skip_categories.definition",
        },
    }),
    "logger.skip_file": BooleanArgument({
        "default": 0,
        "docs": {
            "name": "config.logger.skip_file.name",
        },
    }),
    # Thumbnails
    "thumbnail.width": IntArgument({
        "default": 200,
        "docs": {
            "name": "config.thumbnail.width.name",
        },
    }),
    "thumbnail.height": IntArgument({
        "default": 200,
        "docs": {
            "name": "config.thumbnail.height.name",
        },
    }),
}
