from peewee import Model
from app.App import logger

class BaseModel(Model):
    @classmethod
    def ids(cls, id):
        if type(id) == int or type(id) == str:
            _query = cls.select().where(cls.id == int(id))
            if getattr(cls, "deleted", None) != None:
                _query = _query.where(cls.deleted == 0)

            return _query.first()
        else:
            try:
                __arr = []
                _query = cls.select().where(cls.id << id)
                if getattr(cls, "deleted", None) != None:
                    _query = _query.where(cls.deleted == 0)

                for _e in _query:
                    __arr.append(_e)

                return __arr
            except Exception as exc:
                logger.logException(exc, section = 'Models', silent = False)

                return []
