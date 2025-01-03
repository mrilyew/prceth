from peewee import BigIntegerField, ForeignKeyField, AutoField
from resources.globals import BaseModel

class Relation(BaseModel):
    parent_collection = BigIntegerField(null=True)
    child_collection = ForeignKeyField('collection.Collection', null=True,backref='child_relations')
    child_entity = ForeignKeyField(null=True,backref='relations',model=Entity)
    order = AutoField()
