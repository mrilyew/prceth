from resources.Globals import consts, time, operator, reduce, utils, BaseModel, json5, json, file_manager, logger
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField, JOIN
from db.File import File

class Entity(BaseModel):
    self_name = 'entity'
    __cached_file = None

    id = AutoField() # Absolute id
    file_id = TextField(null=True) # File extension
    linked_files = TextField(null=True) # Files list
    hash = TextField(null=True) # Entity hash
    display_name = TextField(index=True,default='N/A') # Name that shown in list. Set by api
    description = TextField(index=True,null=True) # Description of entity. Set by api
    source = TextField(null=True) # Source of content (URL or path). Set by extractor
    indexation_content_string = TextField(index=True,null=True) # Content that will be used for search. Set by extractor. Duplicates "indexation_content" but without keys.
    # indexation_content = TextField(null=True) # TODO remove Additional info in json (ex. video name)
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    extractor_name = TextField(null=True,default='base') # Extractor that was used for entity
    tags = TextField(index=True,null=True) # csv tags
    preview = TextField(null=True) # Preview in json format
    # flags = IntegerField(default=0) # Flags.
    # type = IntegerField(default=0) # 0 - main is the first file from dir
                                # 1 - main info is from "type_sub" (jsonистый объект)
    entity_internal_content = TextField(null=True,default=None) # DB info type. Format will be taken from "format" (json, xml)
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0) # Is softly deleted
    author = TextField(null=True,default=consts['pc_fullname']) # Author of entity
    declared_created_at = TimestampField(default=time.time())
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True, default=None)
    
    @property
    def orig_source(self):
        p1, p2 = self.source.split(":", 1)

        return p2
    
    @property
    def file(self):
        if self.file_id == None:
            return None
        
        if self.__cached_file != None:
            return self.__cached_file
        
        return File.get(self.file_id)

    def delete(self, delete_dir=True):
        if delete_dir == True:
            file_manager.rmdir(self.getDirPath())

        self.deleted = 1
        self.save()

    # Ну и зачем всё это было. Ладно, может пригодится.
    def getCorrectSource(self):
        from resources.Globals import ExtractorsRepository

        __ext = (ExtractorsRepository()).getByName(self.extractor_name)
        if __ext == None:
            return {"type": "none", "data": {}}

        return __ext().describeSource(INPUT_ENTITY=self)

    def getFormattedInfo(self):
        entity_internal_content = getattr(self, "entity_internal_content", "{}")
        if entity_internal_content == None:
            entity_internal_content = "{}"
        
        return json5.loads(entity_internal_content)

    def getApiStructure(self):
        tags = ",".split(self.tags)
        if tags[0] == ",":
            tags = []
        
        frontend_data = None
        FILE = self.file
        try:
            frontend_data = json5.loads(getattr(self, "frontend_data", "{}"))
        except Exception as wx:
            logger.logException(wx,noConsole=True)
            frontend_data = "{}"
        
        fnl = {
            "id": self.id,
            "has_file": FILE != None,
            "display_name": self.display_name,
            "description": self.description,
            "source": self.getCorrectSource(),
            "meta": self.getFormattedInfo(),
            "frontend_data": frontend_data,
            "tags": tags,
            #"flags": self.flags,
            #"type": self.type,
            "created": self.created_at,
            "declared_created_at": self.declared_created_at,
            "edited": self.edited_at,
            "author": self.author,
        }
        if FILE != None:
            fnl["file"] = FILE.getApiStructure()

        return fnl

    @staticmethod
    def fetchItems(query = None, columns_search = []):
        items = (Entity.select()
                 .where(Entity.unlisted == 0)
                 .where(Entity.deleted == 0)
                 .join(File, on=(File.id == Entity.file_id), join_type=JOIN.LEFT_OUTER))

        conditions = []

        for column in columns_search:
            match column:
                case "upload_name":
                    conditions.append((File.upload_name.contains(query)))
                case "display_name":
                    conditions.append((Entity.display_name.contains(query)))
                case "description":
                    conditions.append((Entity.description.contains(query)))
                case "source":
                    conditions.append((Entity.source.contains(query)))
                case "index":
                    conditions.append((Entity.indexation_content_string.contains(query)))
                case "saved":
                    conditions.append((Entity.extractor_name.contains(query)))
                case "author":
                    conditions.append((Entity.author.contains(query)))
        
        if conditions:
            items = items.where(reduce(operator.or_, conditions))
        
        return items.order_by(Entity.id.desc())
    
    @staticmethod
    def get(id):
        try:
            return Entity.select().where(Entity.id == id).where(Entity.deleted == 0).get()
        except:
            return None

    @staticmethod
    def fromJson(json_input, passed_params):
        FINAL_ENTITY = Entity()
        if json_input.get("hash") == None:
            __hash = utils.getRandomHash(32)
        else:
            __hash = json_input.get("hash")
        
        indexation_content_ = json_input.get("indexation_content")
        entity_internal_content_ = json_input.get("entity_internal_content")

        FINAL_ENTITY.hash = __hash
        if entity_internal_content_ != None:
            FINAL_ENTITY.entity_internal_content = json.dumps(entity_internal_content_)
        else:
            FINAL_ENTITY.entity_internal_content = json.dumps(indexation_content_)
        if json_input.get("file") != None:
            FINAL_ENTITY.file_id = json_input.get("file").id
            FINAL_ENTITY.__cached_file = json_input.get("file")
        
        if json_input.get("unlisted", None) == True:
            FINAL_ENTITY.unlisted = 1

        if json_input.get("linked_files") != None:
            FINAL_ENTITY.linked_files = ",".join(str(v) for v in json_input.get("linked_files"))
        
        FINAL_ENTITY.extractor_name = json_input.get("extractor_name")
        if passed_params.get("display_name") != None:
            FINAL_ENTITY.display_name = passed_params["display_name"]
        else:
            if json_input.get("file") == None:
                if json_input.get("suggested_name") == None:
                    FINAL_ENTITY.display_name = "N/A"
                else:
                    FINAL_ENTITY.display_name = json_input.get("suggested_name")
            else:
                FINAL_ENTITY.display_name = json_input.get("file").upload_name
        
        if passed_params.get("description") != None:
            FINAL_ENTITY.description = passed_params["description"]
        if json_input.get("source") != None:
            FINAL_ENTITY.source = json_input.get("source")
        if json_input.get("indexation_content") != None:
            #FINAL_ENTITY.indexation_content = json_input.dumps(indexation_content_) # remove
            FINAL_ENTITY.indexation_content_string = str(utils.json_values_to_string(indexation_content_)).replace('None', '').replace('  ', ' ').replace('\n', ' ')
        else:
            FINAL_ENTITY.indexation_content_string = json.dumps(utils.json_values_to_string(entity_internal_content_)).replace('None', '').replace('  ', ' ').replace('\n', ' ')
        
        FINAL_ENTITY.save()

        return FINAL_ENTITY
