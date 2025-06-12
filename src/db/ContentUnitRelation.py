from peewee import BigIntegerField, CharField, AutoField, Model, BooleanField

class ContentUnitRelation(Model):
    class Meta:
        table_name = 'content_relations'

    parent = BigIntegerField(null=True)
    child_type = CharField(default='ContentUnit')
    child = BigIntegerField(null=True)
    order = AutoField()
    is_revision = BooleanField(default=0)
