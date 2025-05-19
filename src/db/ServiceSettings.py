from peewee import SmallIntegerField, TextField, AutoField, TimestampField
from resources.Globals import BaseModel, time

class ServiceSettings(BaseModel):
    id = AutoField()
    service_name = TextField()
    display_name = TextField()
    data = TextField(null=True,default=None)
    frontend_data = TextField(null=True,default=None)
    interval = SmallIntegerField(null=True,default=60) # in seconds
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)
