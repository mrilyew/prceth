from peewee import Model
from app.App import logger
import uuid

class BaseModel(Model):
    @classmethod
    def ids(cls, id):
        if type(id) == str:
            _query = cls.select().where(cls.uuid == id)
            if getattr(cls, "deleted", None) != None:
                _query = _query.where(cls.deleted == 0)

            return _query.first()
        else:
            try:
                __arr = []
                _query = cls.select().where(cls.uuid << id)
                if getattr(cls, "deleted", None) != None:
                    _query = _query.where(cls.deleted == 0)

                for _e in _query:
                    __arr.append(_e)

                return __arr
            except Exception as exc:
                logger.logException(exc, section = 'DB', silent = False)

                return []

    @property
    def id(self)->str:
        return self.uuid

    def is_saved(self)->bool:
        return self.id != None

    def save(self, **kwargs):
        self.uuid = str(uuid.uuid4())

        super().save(**kwargs)

    def sign(self)->str:
        return f"__$|{self.short_name}_{self.uuid}"
