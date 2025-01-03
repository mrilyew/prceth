from peewee import Model, SqliteDatabase

DATABASE_PATH = "storage/main.db"
db = SqliteDatabase(DATABASE_PATH)

class BaseModel(Model):
    class Meta:
        database = db
