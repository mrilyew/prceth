from peewee import BigIntegerField, CharField, AutoField, Model, BooleanField

class ContentUnitRelation(Model):
    class Meta:
        table_name = 'content_relations'

    parent = CharField(max_length=100, null=True)
    child_type = CharField(max_length=20, default='ContentUnit')
    child = CharField(max_length=100, null=True)
    order = AutoField()
    is_revision = BooleanField(default=0)
