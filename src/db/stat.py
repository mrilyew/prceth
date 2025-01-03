from peewee import TextField, TimestampField, BigIntegerField, AutoField
from base import BaseModel
from resources.globals import time

class Stat(BaseModel):
    id = AutoField()
    name = TextField(default='Untitled')
    type = TextField(default='default')
    linked_id = BigIntegerField(default=0)
    timestamp = TimestampField(default=time.time())
