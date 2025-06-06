from peewee import SmallIntegerField, BigIntegerField, TextField, AutoField, TimestampField, Model
from utils.MainUtils import parse_json, dump_json
import time

class Service(Model):
    self_name = 'service'

    class Meta:
        table_name = 'services'

    id = AutoField()
    service_name = TextField()
    display_name = TextField(null=True)
    data = TextField(default="{}")
    frontend_data = TextField(default="{}")
    interval = SmallIntegerField(default=60) # in seconds
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)

    def getData(self):
        __data = self.data

        return parse_json(__data)

    def getFrontendData(self):
        __data = self.frontend_data

        return parse_json(__data) 

    def api_structure(self):
        obj = {}

        obj["id"] = self.id
        obj["service_name"] = self.service_name
        obj["display_name"] = self.display_name
        obj["data"] = self.getData()
        obj["frontend_data"] = self.getFrontendData()
        obj["interval"] = self.interval
        obj["created_at"] = self.created_at

        return obj
    
    @staticmethod
    def get(id):
        return Service.select().where(Service.id == id).get()
    
    def updateData(self, json):
        self.data = dump_json(json)
        self.save()
