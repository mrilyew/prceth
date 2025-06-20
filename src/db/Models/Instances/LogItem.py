from peewee import CharField, BigIntegerField, TextField, AutoField, TimestampField, Model
from utils.MainUtils import parse_json, dump_json
import time

class LogItem(Model):
    id = AutoField()
    executable_type = CharField(max_length=30)
    executable_name = CharField(max_length=30)
    args = TextField(default=None,null=True)
    results_count = BigIntegerField(default=0)
    timestamp = TimestampField(default=time.time)
