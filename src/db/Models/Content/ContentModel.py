from peewee import Model
from snowflake import SnowflakeGenerator
from app.App import logger

class BaseModel(Model):
    @classmethod
    def ids(cls, id):
        _type = type(id)

        if _type == str:
            _query = cls.select().where(cls.uuid == id)

            return _query.first()

        if _type == list:
            res = []
            _query = cls.select().where(cls.uuid.in_(id))

            for _e in _query:
                res.append(_e)

            return res

    @property
    def id(self)->str:
        return self.uuid

    def is_saved(self)->bool:
        return self.uuid != None

    def save(self, **kwargs):
        gen = SnowflakeGenerator(0)
        self.uuid = str(next(gen))

        super().save(**kwargs)

    def sign(self)->str:
        return f"__$|{self.short_name}_{self.uuid}"
