from peewee import BigIntegerField, ForeignKeyField, AutoField
from base import BaseModel
from collection import Collection
from entity import Entity

class Relation(BaseModel):
    parent_collection = BigIntegerField(null=True)
    child_collection = ForeignKeyField(null=True,backref='child_relations',model=Collection)
    child_entity = ForeignKeyField(null=True,backref='relations',model=Entity)
    order = AutoField()
