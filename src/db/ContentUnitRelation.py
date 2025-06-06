from peewee import BigIntegerField, DeferredForeignKey, AutoField, Model

class ContentUnitRelation(Model):
    parent = BigIntegerField(null=True)
    child = DeferredForeignKey('ContentUnit', null=True,backref='relations')
    order = AutoField()
