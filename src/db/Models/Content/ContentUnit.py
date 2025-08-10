from db.Models.Content.ThumbnailState import ThumbnailState
from utils.MainUtils import dump_json, parse_json
from peewee import TextField, CharField, BooleanField, FloatField, IntegerField
from db.Models.Content.ContentModel import BaseModel
from db.Models.Content.StorageUnit import StorageUnit
from functools import cached_property
import os, json, datetime

class ContentUnit(BaseModel):
    '''
    Model that represents unit of information
    '''

    class Meta:
        table_name = 'content_units'

    self_name = 'ContentUnit'
    short_name = 'cu'

    # Identification
    uuid = IntegerField(unique=True, primary_key=True)

    # Data
    content = TextField(null=True, default=None) # JSON data
    representation = TextField(null=True)
    storage_unit = CharField(null=True,max_length=100)
    extractor = TextField(null=True, default=None) # Extractor that was used for creation

    # Display
    display_name = TextField(default='N/A')
    description = TextField(index=True, null=True)
    source = TextField(null=True)
    # frontend_data = TextField(null=True) # Currently unused
    # tags = TextField(index=True,null=True) # это вообще отдельной таблицей должно
    outer = TextField(null=True) # frontend data (with thumbnail)
    # author = TextField(null=True,default=consts.get('pc_fullname')) под вопросом

    # Dates
    declared_created_at = FloatField()
    created_at = FloatField()
    edited_at = FloatField(default=None,null=True)

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0)

    link_queue = []

    # Properties

    @cached_property
    def json_content(self):
        return parse_json(self.content)

    @cached_property
    def main_su(self):
        if self.storage_unit != None:
            su = StorageUnit.ids(self.storage_unit)

            return su

        return None

    @cached_property
    def linked_list(self):
        from db.LinkManager import link_manager

        list = link_manager.linksList(self)

        return list

    # Content

    def formatted_data(self, recursive = False, recurse_level = 0):
        from db.LinkManager import link_manager

        loaded_content = self.json_content

        if recursive == True and recurse_level < 3:
            loaded_content = link_manager.injectLinksToJsonFromInstance(self, recurse_level)

        return loaded_content

    def update_data(self, new_data: dict):
        cnt = self.json_content
        cnt.update(new_data)

        self.content = json.dumps(cnt, ensure_ascii=False)

    def set_thumbnail(self, thumbs):
        thumbs_out = []

        if thumbs:
            for __ in thumbs:
                thumbs_out.append(__.state())

        self.outer = json.dumps({"thumbnail": thumbs_out}, ensure_ascii=False)

    @cached_property
    def thumbnail_list(self):
        _outer = parse_json(self.outer)
        _thumb = _outer.get("thumbnail")
        if _thumb == None:
            return []

        _list = []

        for thmb in _thumb:
            _list.append(ThumbnailState(thmb))

        return _list

    def api_structure(self, return_content = True, sensitive=False):
        ret = {}
        ret['id'] = str(self.uuid) # Converting to str cuz js function JSON.parse cannot convert it
        ret['display_name'] = self.display_name
        ret['description'] = self.description
        ret['representation'] = self.representation
        ret['extractor'] = self.extractor
        # ret['tags'] = self.get_tags()

        if return_content == True:
            ret['content'] = self.formatted_data(recursive=True)

        if self.source != None:
            ret['source'] = parse_json(self.source)

        if self.outer != None:
            try:
                ret['outer'] = parse_json(self.outer)

                # у меня абсолютно нет идей для названия переменных ((
                thumbnail_internal_classes_from_db_list = self.thumbnail_list
                thumbnail_api_response_list = []

                for iterated_thumbnail in thumbnail_internal_classes_from_db_list:
                    thumbnail_api_response_list.append(iterated_thumbnail.api_structure())

                ret['thumbnail'] = thumbnail_api_response_list
            except Exception as e:
                print(e)
                pass

        try:
            # cuz after saving it doesnt converts to datetime we need to use this workaround
            if getattr(self.created_at, 'timestamp', None) != None:
                ret["created"] = float(self.created_at.timestamp())
            else:
                ret["created"] = float(self.created_at)

            if self.edited_at != None:
                if getattr(self.edited_at, 'timestamp', None) != None:
                    ret["edited"] = float(self.edited_at.timestamp())
                else:
                    ret["edited"] = float(self.edited_at)

            if getattr(self.declared_created_at, 'timestamp', None) != None:
                ret["declared_created"] = float(self.declared_created_at.timestamp())
            else:
                ret["declared_created"] = float(self.declared_created_at)
        except Exception as _e:
            print(_e)

        return ret

    def set_source(self, source_json: dict):
        self.source = dump_json(source_json)

    def save_info_to_json(self, dir_path):
        with open(os.path.join(dir_path, f"data_{self.uuid}.json"), "w", encoding='utf8') as json_file:
            json_file.write(json.dumps(self.api_structure(sensitive=True), indent=2, ensure_ascii=False))

    def save(self, **kwargs):
        self.created_at = float(datetime.datetime.now().timestamp())

        if getattr(self, "declared_created_at", None) == None:
            self.declared_created_at = float(datetime.datetime.now().timestamp())

        super().save(**kwargs)

        if self.link_queue != None:
            from db.LinkManager import link_manager

            for item in self.link_queue:
                if item == None:
                    continue

                try:
                    link_manager.link(self, item)
                except AssertionError:
                    pass
