from peewee import Model
from app.App import logger

class BaseModel(Model):
    @classmethod
    def ids(cls, id):
        if type(id) == int:
            try:
                return cls.select().where(cls.id == id).where(cls.deleted == 0).get()
            except:
                return None
        else:
            try:
                __arr = []
                for _e in cls.select().where(cls.id << id).where(cls.deleted == 0):
                    __arr.append(_e)

                return __arr
            except Exception as exc:
                logger.logException(exc, section = 'Models', silent = False)

                return []
