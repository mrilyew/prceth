import os, time, json5, json
from utils.MainUtils import dump_json, parse_json, replace_link_gaps, get_random_hash, clear_json, json_values_to_string, parse_db_entities
from peewee import TextField, IntegerField, CharField, BooleanField, TimestampField
from db.Models.Content.StorageUnit import StorageUnit
from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from db.Models.Content.ContentModel import BaseModel
from functools import cached_property
from app.App import logger

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
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    tags = TextField(index=True,null=True)
    thumbnail = TextField(null=True) # Preview in json format
    # author = TextField(null=True,default=consts.get('pc_fullname')) значимость под вопросом

    # Dates
    declared_created_at = TimestampField(default=time.time())
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)

    # Files
    su_id = IntegerField(null=True) # File id

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0)

    # Cached
    __tmpLinks = None
    __cached_links = {}
    __cached_su = None
    __cached_content = None

    # Properties

    @cached_property
    def json_content(self):
        return parse_json(self.content)

    @cached_property
    def su(self):
        if self.su_id == None:
            return None

        _su = StorageUnit.select().where(StorageUnit.uuid == self.su_id).first()

        return _su

    @cached_property
    def linked_units(self):
        __out = ContentUnitRelation.select().where(ContentUnitRelation.child << self._linksSelectionIds())

        return __out

    # Recievation

    def formatted_data(self, recursive = False, recurse_level = 0):
        loaded_content = self.json_content

        if recursive == True and recurse_level < 3:
            loaded_content = replace_link_gaps(input_data=loaded_content,
                                               link_to_linked_files=self.linked_units,
                                               recurse_level=recurse_level)

        return loaded_content

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
            "id": self.uuid,
            "display_name": self.display_name,
            "description": self.description,
            "meta": self.formatted_data(recursive=True),
            "frontend_data": frontend_data,
            "tags": tags,
            "created": None,
            "edited": None,
            "declared_created_at": None
        }

        if self.source != None:
            fnl['source'] = parse_json(self.source)

        try:
            fnl["created"] = int(self.created_at)
            fnl["edited"] = int(self.edited_at)
            fnl["declared_created_at"] = str(self.declared_created_at)
        except Exception:
            pass

        if sensitive == False and __su != None:
            fnl["file"] = __su.api_structure()

        return fnl

    def cli_show(self):
        return f"{self.display_name}, {int(self.declared_created_at)}"

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

        out.extractor = json_input.get("extractor")
        out.representation = json_input.get("representation")

        if json_input.get("display_name") != None:
            out.display_name = json_input.get('display_name')
        else:
            if json_input.get("name") == None:
                if json_input.get("file") == None:
                    out.display_name = "N/A"
                else:
                    out.display_name = json_input.get('file').upload_name
            else:
                out.display_name = json_input.get('name')

        if json_input.get("description") != None:
            out.description = json_input.get('description')
        if json_input.get("source") != None:
            out.set_source(json_input.get('source'))
        if json_input.get("declared_created_at") != None:
            if getattr(json_input.get("declared_created_at"), 'timestamp', None) != None:
                out.declared_created_at = int(json_input.get("declared_created_at").timestamp())
            else:
                out.declared_created_at = int(json_input.get("declared_created_at"))

        # out.indexation_content_string = json.dumps(json_values_to_string(content), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        if json_input.get('is_collection', False) == True:
            out.is_collection = True

        if json_input.get('make_thumbnail', False) == True:
            thmb = out.make_thumbnail({}, json_input.get('representation_class', None))
            if thmb != None:
                fnl = []
                for t in thmb:
                    fnl.append(t.data)

                out.thumbnail = dump_json(fnl)

        if json_input.get('save_model', False) == True:
            out.save(force_insert=True)

        if json_input.get("links") != None:
            __links = []
            for item in json_input.get("links"):
                __links.append(item)

            if len(__links) > 0:
                out.__tmpLinks = __links

        return out

    def save(self, **kwargs):
        super().save(**kwargs)

        if self.__tmpLinks != None:
            __links = []

            for item in self.__tmpLinks:
                if item == None:
                    continue

                self.addLink(item)
                __links.append(item)

            self.__cached_links = __links

    def set_source(self, source_json: dict):
        self.source = dump_json(source_json)

    def make_thumbnail(self, i = {}, representation = None):
        if representation != None and getattr(representation, 'preview', None) != None:
            return representation.preview({})

        main_file = self.su

        if main_file != None:
            return main_file.make_thumbnail(i)

    # Links

    def addLink(self, u):
        if u == None:
            logger.log(message=f"Not found item to link", section='DB', kind = logger.KIND_ERROR)
            return

        _link = ContentUnitRelation()
        _link.parent = self.uuid
        _link.child_type = u.__class__.__name__
        _link.child = u.uuid

        logger.log(message=f"Linked {self.short_name}_{self.uuid}<->{u.short_name}_{u.uuid}", section='DB', kind = logger.KIND_SUCCESS)

        _link.save()

    def removeLink(self, u):
        if u == None:
            logger.log(message=f"Not found item to link", section='DB', kind = logger.KIND_ERROR)
            return

        _link = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.uuid).where(ContentUnitRelation.child == u.uuid).where(ContentUnitRelation.child_type == u.__class__.__name__)

        logger.log(message=f"Unlinked {self.short_name}_{self.uuid}<->{u.short_name}_{u.uuid}", section='DB', kind = logger.KIND_SUCCESS)

        _link.delete()

    def _linksSelection(self, class_name = 'CollectionUnit'):
        _links = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.uuid).where(ContentUnitRelation.child_type == class_name)

        return _links

    def _linksSelectionIds(self, class_name = 'CollectionUnit'):
        _selection = self._linksSelection(class_name)

        ids = []
        for unit in _selection:
            ids.append(unit.child)

        return ids

    def bifurcation(self, level=0, maximum=3):
        connections = {}

        __links = self.linked_units
        for link in __links:
            if level > maximum:
                continue

            connections[level] = link.bifurcation(level+1, maximum)

        return connections

    # Actions

    def delete(self):
        # TODO additional options
        super().delete()

    def save_info_to_json(self, dir_path):
        with open(os.path.join(dir_path, f"data_{self.id}.json"), "w", encoding='utf8') as json_file:
            json_file.write(json.dumps(self.api_structure(sensitive=True), indent=2, ensure_ascii=False))

    async def export(self, **kwargs):
        dir_path = kwargs.get('dir_path')
        file_prefix = kwargs.get('file_prefix', '')
        recursion_level = kwargs.get('recursion_level', 0)
        recursion_level_limit = kwargs.get('recursion_level_limit', 5)
        save_json = kwargs.get('save_json', False)
        if recursion_level > recursion_level_limit:
            return None

        main_su = self.su
        if main_su != None:
            await main_su.export(dir_path, kwargs.get('file_prefix', ''))

        if kwargs.get('export_linked', True) == True:
            links = self.linked_units
            for link in links:
                link.export(dir_path=dir_path,save_json=save_json,recursion_level=recursion_level+1,recursion_level_limit=recursion_level_limit)

        if save_json == True:
            self.save_info_to_json(dir_path)
