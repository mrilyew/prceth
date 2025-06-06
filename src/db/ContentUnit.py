import os, time, operator, json5, json
from pathlib import Path
from submodules.Files.FileManager import file_manager
from resources.Consts import consts
from utils.MainUtils import replace_link_gaps, get_random_hash, clear_json, json_values_to_string, parse_db_entities
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField, JOIN
from db.StorageUnit import StorageUnit
from functools import reduce
from db.BaseModel import BaseModel
from app.App import logger

class ContentUnit(BaseModel):
    '''
    Model that represents unit of information.

    Fields:
    id: id of ContentUnit
    content: json content of ContentUnit
    display_name: visual name of ContentUnit

    '''

    class Meta:
        table_name = 'content_units'

    self_name = 'ContentUnit'

    # Identification
    id = AutoField() # Absolute id
    hash = TextField(null=True)

    # Data
    content = TextField(null=True,default=None) # JSON data
    representation = TextField(null=True,default='File')
    extractor = TextField(null=True,default=None) # Extractor that was used for creation
    preview = TextField(null=True) # Preview in json format

    # Meta
    display_name = TextField(index=True,default='N/A')
    description = TextField(index=True,null=True)
    source = TextField(null=True) # Source of content in JSON format
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    tags = TextField(index=True,null=True) # csv tags
    author = TextField(null=True,default=consts.get('pc_fullname'))

    # Dates
    declared_created_at = TimestampField(default=time.time())
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)

    # Files
    su_id = IntegerField(null=True) # File id
    links = TextField(null=True) # Files list

    # Visibility
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0)

    @property
    def file(self):
        if self.su_id == None:
            return None

        if self.__cached_su != None:
            return self.__cached_su

        _fl = StorageUnit.get(self.su_id)
        self.__cached_su = _fl
        
        return _fl

    def delete(self):
        # TODO additional options
        super().delete()

    def formatted_data(self, recursive = False, recurse_level = 0):
        content = getattr(self, "content", {})
        loaded_content = json5.loads(content)

        if recursive == True and recurse_level < 3:
            loaded_content = replace_link_gaps(input_data=loaded_content,
                                               link_to_linked_files=self.linked_entities,
                                               recurse_level=recurse_level)

        return loaded_content

    @property
    def linked_entities(self):
        if self.__cachedLinks != None:
            return self.__cachedLinks

        if self.links == None:
            return []

        _out = parse_db_entities(self.links)
        
        self.__cachedLinks = _out

        return _out
    
    def api_structure(self, sensitive=False):
        tags = ",".split(self.tags)
        if tags[0] == ",":
            tags = []

        frontend_data = None
        FILE = self.file
        try:
            frontend_data = json5.loads(getattr(self, "frontend_data", "{}"))
        except Exception as wx:
            logger.logException(wx,silent=True)
            frontend_data = "{}"
        
        fnl = {
            "id": self.id,
            "has_file": FILE != None,
            "display_name": self.display_name,
            "description": self.description,
            "source": self.getCorrectSource(),
            "meta": self.getFormattedInfo(recursive=True),
            "frontend_data": frontend_data,
            "tags": tags,
            "author": self.author,
            "created": None,
            "edited": None,
            "declared_created_at": None
        }

        try:
            fnl["created"] = int(self.created_at)
            fnl["edited"] = int(self.edited_at)
            fnl["declared_created_at"] = str(self.declared_created_at)
        except Exception:
            pass

        if sensitive == False and FILE != None:
            fnl["file"] = FILE.api_structure()

        return fnl

    @staticmethod
    def fromJson(json_input, passed_params):
        __hash = get_random_hash(32)
