from peewee import BigIntegerField, DeferredForeignKey, AutoField, Model

class ContentUnitRelation(Model):
    class Meta:
        table_name = 'content_relations'

    parent = BigIntegerField(null=True)
    child = DeferredForeignKey('ContentUnit', null=True,backref='relations')
    order = AutoField()
