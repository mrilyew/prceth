import os, time, operator, json5, json
from pathlib import Path
from submodules.Files.FileManager import file_manager
from resources.Consts import consts
from utils.MainUtils import dump_json, parse_json, replace_link_gaps, get_random_hash, clear_json, json_values_to_string, parse_db_entities
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField, JOIN
from db.StorageUnit import StorageUnit
from db.BaseModel import BaseModel
from functools import reduce
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
    #hash = TextField(null=True)

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

    # Useless
    __cachedLinks = {}
    __cached_su = {}
    __cached_content = None

    @property
    def json_content(self):
        if self.__cached_content != None:
            return self.__cached_content
        if self.content == None:
            return {}

        return parse_json(self.content)

    @property
    def su(self):
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
        loaded_content = self.json_content

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
        __su = self.su
        try:
            frontend_data = json5.loads(getattr(self, "frontend_data", "{}"))
        except Exception as wx:
            frontend_data = {}
        
        fnl = {
            "id": self.id,
            "has_file": __su != None,
            "display_name": self.display_name,
            "description": self.description,
            "meta": self.formatted_data(recursive=True),
            "frontend_data": frontend_data,
            "tags": tags,
            "author": self.author,
            "created": None,
            "edited": None,
            "declared_created_at": None
        }

        if self.source != None:
            fnl.source = parse_json(self.source)

        try:
            fnl["created"] = int(self.created_at)
            fnl["edited"] = int(self.edited_at)
            fnl["declared_created_at"] = str(self.declared_created_at)
        except Exception:
            pass

        if sensitive == False and __su != None:
            fnl["file"] = __su.api_structure()

        return fnl

    @staticmethod
    def fromJson(json_input):
        out = ContentUnit()
        '''
        if json_input.get("hash") == None:
            __hash = get_random_hash(32)
        else:
            __hash = json_input.get("hash")
        '''

        content = json_input.get("content")
        if content != None:
            out.content = dump_json(content)

        if json_input.get("main_su") != None:
            out.su_id = json_input.get("main_su").id
            out.__cached_su = json_input.get("main_su")

        if json_input.get("unlisted", None) == True:
            out.unlisted = 1

        if json_input.get("links") != None:
            __out = []
            for item in json_input.get("links"):
                if item == None:
                    continue

                __out.append(f"{item.self_name}_{item.id}")

            if len(__out) > 0:
                out.links = ",".join(__out)
                out.__cachedLinks = json_input.get("linked_files")

        out.extractor = json_input.get("extractor")
        out.representation = json_input.get("representation")

        if json_input.get("display_name") != None:
            out.display_name = json_input.get('display_name')
        else:
            if json_input.get("suggested_name") == None:
                if json_input.get("file") == None:
                    out.display_name = "N/A"
                else:
                    out.display_name = json_input.get('file').upload_name
            else:
                out.display_name = json_input.get('suggested_name')

        if json_input.get("description") != None:
            out.description = json_input.get('description')
        if json_input.get("source") != None:
            out.source = dump_json(json_input.get('source'))
        if json_input.get("declared_created_at") != None:
            out.declared_created_at = int(json_input.get("declared_created_at"))

        # out.indexation_content_string = json.dumps(json_values_to_string(content), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        if json_input.get('save_model', False) == True:
            out.save()

        return out
