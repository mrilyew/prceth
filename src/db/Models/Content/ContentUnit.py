import os, time, json5, json
from utils.MainUtils import dump_json, parse_json, replace_link_gaps
from peewee import TextField, CharField, BooleanField, TimestampField
from db.Models.Content.ContentModel import BaseModel
from functools import cached_property

class ContentUnit(BaseModel):
    '''
    Model that represents unit of information
    '''

    class Meta:
        table_name = 'content_units'

    self_name = 'ContentUnit'
    short_name = 'cu'

    # Identification
    uuid = CharField(max_length=50, unique=True, primary_key=True) # UUID

    # Data
    content = TextField(null=True, default=None) # JSON data
    representation = TextField(null=True)
    extractor = TextField(null=True, default=None) # Extractor that was used for creation

    # Display
    display_name = TextField(default='N/A')
    description = TextField(index=True, null=True)
    source = TextField(null=True)
    # frontend_data = TextField(null=True) # Currently unused
    # tags = TextField(index=True,null=True) # это вообще отдельной таблицей должно
    thumbnail = TextField(null=True) # Preview in json format
    # author = TextField(null=True,default=consts.get('pc_fullname')) под вопросом

    # Dates
    declared_created_at = TimestampField(default=time.time())
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0)

    link_queue = []

    # Properties

    @cached_property
    def json_content(self):
        return parse_json(self.content)

    # Recievation

    def formatted_data(self, recursive = False, recurse_level = 0):
        from db.LinkManager import link_manager

        loaded_content = self.json_content

        if recursive == True and recurse_level < 3:
            loaded_content = replace_link_gaps(input_data=loaded_content,
                                               link_to_linked_files=link_manager.linksList(self),
                                               recurse_level=recurse_level)

        return loaded_content

    # unused at this moment
    def fr_data(self):
        frontend_data = None
        try:
            frontend_data = json5.loads(getattr(self, "frontend_data", "{}"))
        except Exception as wx:
            frontend_data = {}

        return frontend_data

    def get_tags(self):
        tags = ",".split(self.tags)
        if tags[0] == ",":
            tags = []

        return tags

    def api_structure(self, sensitive=False):
        ret = {}
        ret['id'] = self.uuid
        ret['display_name'] = self.display_name
        ret['description'] = self.description
        ret['content'] = self.formatted_data(recursive=True)
        # ret['tags'] = self.get_tags()

        if self.source != None:
            ret['source'] = parse_json(self.source)

        try:
            ret["created"] = int(self.created_at)
            ret["edited"] = int(self.edited_at)
            ret["declared_created_at"] = str(self.declared_created_at)
        except Exception:
            pass

        return ret

    def set_source(self, source_json: dict):
        self.source = dump_json(source_json)

    def make_thumbnail(self, i = {}, representation = None):
        if representation != None and getattr(representation, 'preview', None) != None:
            return representation.preview({})

        main_file = self.su

        if main_file != None:
            return main_file.make_thumbnail(i)

    def save_info_to_json(self, dir_path):
        with open(os.path.join(dir_path, f"data_{self.uuid}.json"), "w", encoding='utf8') as json_file:
            json_file.write(json.dumps(self.api_structure(sensitive=True), indent=2, ensure_ascii=False))

    def save(self, **kwargs):
        super().save(**kwargs)

        if self.link_queue != None:
            from db.LinkManager import link_manager

            for item in self.link_queue:
                if item == None:
                    continue

                link_manager.link(self, item)
