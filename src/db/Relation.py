from peewee import BigIntegerField, DeferredForeignKey, AutoField, Model

class Relation(Model):
    parent_collection_id = BigIntegerField(null=True)
    child_collection_id = DeferredForeignKey('Collection', null=True,backref='child_relations')
    child_ContentUnit_id = DeferredForeignKey('ContentUnit', null=True,backref='relations')
    order = AutoField()
