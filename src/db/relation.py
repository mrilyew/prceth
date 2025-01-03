from peewee import BigIntegerField, DeferredForeignKey, AutoField
from resources.globals import BaseModel

class Relation(BaseModel):
    parent_collection = BigIntegerField(null=True)
    child_collection = DeferredForeignKey('Collection', null=True,backref='child_relations')
    child_entity = DeferredForeignKey('Entity', null=True,backref='relations')
    order = AutoField()
