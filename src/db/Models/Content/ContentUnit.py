from db.Models.Content.ThumbnailState import ThumbnailState
from resources.Exceptions import AlreadyLinkedException
from utils.MainUtils import dump_json, parse_json
from peewee import TextField, CharField, BooleanField, FloatField, IntegerField
from db.Models.Content.ContentModel import BaseModel
from db.Models.Content.StorageUnit import StorageUnit
from functools import cached_property
import os, json, datetime
from app.App import logger

class ContentUnit(BaseModel):
    # Identification
    uuid = IntegerField(unique=True, primary_key=True)

    # Display
    display_name = TextField(default='N/A')
    description = TextField(index=True, null=True)
    # author = TextField(null=True,default=consts.get('pc_fullname')) под вопросом

    # Data
    content = TextField(null=True, default=None) # JSON data
    source = TextField(null=True)
    outer = TextField(null=True, default=None) # frontend data (with thumbnail)
    saved = TextField(null=True, default=None)

    # Links
    storage_unit = CharField(null=True,max_length=100)

    # Dates
    declared_created_at = FloatField()
    created_at = FloatField()
    edited_at = FloatField(default=None,null=True)

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    is_unlisted = BooleanField(index=True,default=0)
    # is_deleted = BooleanField(index=True,default=0)

    # so the class
    class Meta:
        table_name = 'content_units'

    self_name = 'ContentUnit'
    short_name = 'cu'
    link_queue = None
    via_method = None

    # Properties

    @cached_property
    def content_json(self):
        if self.content == None:
            return {}

        return parse_json(self.content)

    @cached_property
    def outer_json(self):
        if self.outer == None:
            return {}

        return parse_json(self.outer)

    @cached_property
    def source_json(self):
        if self.source == None:
            return {}

        return parse_json(self.source)

    @cached_property
    def saved_json(self):
        if self.saved == None:
            return {}

        return parse_json(self.saved)

    def update_data(self, new_data: dict):
        cnt = self.content_json
        cnt.update(new_data)

        self.content = json.dumps(cnt, ensure_ascii=False)

    def data_with_linked_replacements(self, recursive = False, recurse_level = 0):
        from db.LinkManager import LinkManager

        loaded_content = self.content_json
        if recursive == True and recurse_level < 3:
            link_manager = LinkManager(self)
            loaded_content = link_manager.injectLinksToJsonFromInstance(recurse_level)

        return loaded_content

    @cached_property
    def thumbnail_list(self):
        _thumb = self.outer_json.get("thumbnail")
        if _thumb == None:
            return []

        _list = []

        for thmb in _thumb:
            _list.append(ThumbnailState(thmb))

        return _list

    def set_thumbnail(self, thumbs):
        thumbs_out = []

        if thumbs:
            for __ in thumbs:
                thumbs_out.append(__.state())

        write_this = {}
        if len(thumbs_out) > 0:
            write_this["thumbnail"] = thumbs_out

        self.outer = json.dumps(write_this, ensure_ascii=False)

    def set_source(self, source_json: dict):
        self.source = dump_json(source_json)

    @cached_property
    def common_link(self):
        if self.storage_unit != None:
            su = StorageUnit.ids(self.storage_unit)

            return su

        return None

    @cached_property
    def linked_list(self):
        from db.LinkManager import LinkManager

        link_manager = LinkManager(self)
        list = link_manager.linksList(self)

        return list

    # it will be saved later
    def add_link(self, item):
        if self.link_queue is None:
            self.link_queue = []
        self.link_queue.append(item)

    def write_link_queue(self):
        from db.LinkManager import LinkManager

        link_manager = LinkManager(self)

        for item in self.link_queue:
            if item == None:
                continue

            try:
                link_manager.link(item)
            except AssertionError as _e:
                logger.log(message=f"Failed to link: {str(_e)}", section=logger.SECTION_LINKAGE, kind = logger.KIND_ERROR)
            except AlreadyLinkedException as _e:
                logger.log(message=f"Failed to link: {str(_e)}", section=logger.SECTION_LINKAGE, kind = logger.KIND_ERROR)

        self.link_queue = None

    def set_common_link(self, item):
        self.storage_unit = item.uuid

    def set_saved(self, save_json: dict):
        self.saved = dump_json(save_json)

    def mark_representation(self, method):
        saved_json = {
            "method": method.full_name(),
            "representation": method.outer.full_name()
        }

        self.via_method = method
        self.set_saved(saved_json)

    def api_structure(self, return_content = True, sensitive=False):
        payload = {}
        payload['class_name'] = "ContentUnit"
        payload['id'] = str(self.uuid) # Converting to str cuz JSON.parse cannot convert it
        payload['display_name'] = self.display_name
        payload['description'] = self.description
        payload['source'] = self.source_json
        payload['saved'] = self.saved_json
        # ret['tags'] = self.get_tags()

        if return_content == True:
            payload['content'] = self.data_with_linked_replacements(recursive=True)

        if self.outer != None:
            try:
                payload['outer'] = self.outer_json

                # у меня абсолютно нет идей для названия переменных ((
                thumbnail_internal_classes_from_db_list = self.thumbnail_list
                thumbnail_api_response_list = []

                for iterated_thumbnail in thumbnail_internal_classes_from_db_list:
                    thumbnail_api_response_list.append(iterated_thumbnail.api_structure())

                payload['outer']['thumbnail'] = thumbnail_api_response_list
            except Exception as e:
                print(e)
                pass

        try:
            # it does not converts to datetime after saving so we need to use this workaround
            if getattr(self.created_at, 'timestamp', None) != None:
                payload["created"] = float(self.created_at.timestamp())
            else:
                payload["created"] = float(self.created_at)

            if self.edited_at != None:
                if getattr(self.edited_at, 'timestamp', None) != None:
                    payload["edited"] = float(self.edited_at.timestamp())
                else:
                    payload["edited"] = float(self.edited_at)

            if getattr(self.declared_created_at, 'timestamp', None) != None:
                payload["declared_created"] = float(self.declared_created_at.timestamp())
            else:
                payload["declared_created"] = float(self.declared_created_at)
        except Exception as _e:
            print(_e)

        return payload

    def save_info_to_json(self, dir_path):
        with open(os.path.join(dir_path, f"data_{self.uuid}.json"), "w", encoding='utf8') as json_file:
            json_file.write(json.dumps(self.api_structure(sensitive=True), indent=2, ensure_ascii=False))

    def save(self, **kwargs):
        kwargs["force_insert"] = True

        make_thumbnail = True

        self.created_at = float(datetime.datetime.now().timestamp())

        if getattr(self, "content", None) != None and type(self.content) != str:
            self.content = dump_json(self.content)

        if getattr(self, "source", None) != None and type(self.source) != str:
            self.source = dump_json(self.source)

        if self.via_method != None:
            if make_thumbnail == True:
                thumb_class = self.via_method.outer.Thumbnail(self.via_method)
                thumb_out = thumb_class.create(self, {})

                self.set_thumbnail(thumb_out)

        if getattr(self, "declared_created_at", None) == None:
            self.declared_created_at = float(datetime.datetime.now().timestamp())

        super().save(**kwargs)

        if self.link_queue != None:
            self.write_link_queue()
