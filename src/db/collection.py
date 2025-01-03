from peewee import TextField, IntegerField, AutoField, BooleanField, TimestampField, JOIN
from resources.globals import BaseModel, consts, time

class Collection(BaseModel):
    self_name = 'collection'

    id = AutoField()
    name = TextField(index=True,default='...')
    description = TextField(index=True,null=True)
    order = IntegerField(null=True,default=0)
    author = TextField(null=True,default=consts['pc_fullname'])
    frontend_type = TextField(default='list',null=False)
    json_info = TextField(index=True,null=True)
    icon_hash = TextField(null=True)
    hidden = BooleanField(default=0)
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True, default=0)
    
    @staticmethod
    def getAll():
        results = Collection.select().where(Collection.hidden == 0).order_by(Collection.order).dicts()
        result_entities = []

        for entity in results:
            result_entities.append(Collection(**entity))
        
        return result_entities
    
    @staticmethod
    def getAllCount():
        return Collection.select().where(Collection.hidden == 0).count()
    
    @staticmethod
    def get(id):
        try:
            return Collection.select().where(Collection.id == id).get()
        except:
            return None
    
    def takeInfo(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "order": self.order,
            "inner_type": self.innertype,
            "icon_hash": self.icon_hash,
            "created": self.created_at,
            "edited": self.edited_at,
            "count": self.getItemsCount(),
        }
    
    def switch(self, to_switch):
        f_order = self.order
        s_order = to_switch.order

        self.order = s_order
        to_switch.order = f_order

        self.save()
        to_switch.save()

