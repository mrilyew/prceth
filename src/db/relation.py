from peewee import BigIntegerField, DeferredForeignKey, AutoField
from resources.globals import BaseModel

class Relation(BaseModel):
    parent_collection_id = BigIntegerField(null=True)
    child_collection_id = DeferredForeignKey('Collection', null=True,backref='child_relations')
    child_entity_id = DeferredForeignKey('Entity', null=True,backref='relations')
    order = AutoField()
