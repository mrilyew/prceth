from peewee import Model, SqliteDatabase
from resources.Globals import config, consts

DATABASE_PATH = config.get("db.path").replace("?cwd?", consts.get("cwd").replace("\\src", ""))
db = SqliteDatabase(DATABASE_PATH)

class BaseModel(Model):
    class Meta:
        database = db
