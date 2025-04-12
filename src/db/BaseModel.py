from peewee import Model, SqliteDatabase
from submodules.Config import config

DATABASE_PATH = config.get("db.path")
db = SqliteDatabase(DATABASE_PATH)

class BaseModel(Model):
    class Meta:
        database = db
