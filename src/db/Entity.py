from resources.Globals import Path, os, consts, time, operator, utils, BaseModel, json5, json, file_manager, logger
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField, JOIN
from db.File import File
from functools import reduce

class Entity(BaseModel):
    self_name = 'entity'
    __cached_file = None
    __cachedLinkedEntities = None

    id = AutoField() # Absolute id
    internal_content = TextField(null=True,default=None)
    display_name = TextField(index=True,default='N/A') # Name that shown in list. Set by api
    description = TextField(index=True,null=True) # Description of entity. Set by api
    source = TextField(null=True) # Source of content (URL or path). Set by extractor
    frontend_data = TextField(null=True) # Info that will be used in frontend. Set by frontend.
    tags = TextField(index=True,null=True) # csv tags
    file_id = IntegerField(null=True) # File id
    linked_files = TextField(null=True) # Files list
    # hash = TextField(null=True) # Entity hash
    # indexation_content = TextField(null=True) # TODO remove Additional info in json (ex. video name)
    extractor_name = TextField(null=True,default='base') # Extractor that was used for entity
    preview = TextField(null=True) # Preview in json format
    # flags = IntegerField(default=0) # Flags.
    # type = IntegerField(default=0) # 0 - main is the first file from dir
                                    # 1 - main info is from "type_sub" (jsonистый объект)
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0) # Is softly deleted
    author = TextField(null=True,default=consts.get('pc_fullname')) # Author of entity
    declared_created_at = TimestampField(default=time.time())
    created_at = TimestampField(default=time.time())
    edited_at = TimestampField(null=True)
    indexation_content_string = TextField(index=True,null=True) # Content that will be used for search. Set by extractor. Duplicates "indexation_content" but without keys.
    
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

        _fl = File.get(self.file_id)
        self.__cached_file = _fl
        
        return _fl

    def delete(self, delete_dir=False):
        if delete_dir == True:
            if self.file != None:
                file_manager.rmdir(self.file.getDirPath())

        super().delete()
    
    def getCorrectSource(self):
        from resources.Globals import ExtractorsRepository

        __ext = (ExtractorsRepository()).getByName(self.extractor_name)
        if __ext == None:
            return {"type": "none", "data": {}}

        return __ext().describeSource(INPUT_ENTITY=self)

    def getFormattedInfo(self, recursive = False, recurse_level = 0):
        internal_content = getattr(self, "internal_content", "{}")
        if internal_content == None:
            internal_content = "{}"
        
        lods_ = json5.loads(internal_content)
        if recursive == True and recurse_level < 3:
            linked_files = self.getLinkedEntities()
            lods_ = utils.replaceStringsInDict(input_data=lods_,link_to_linked_files=linked_files,recurse_level=recurse_level)

        return lods_

    def getLinkedEntities(self):
        if self.__cachedLinkedEntities != None:
            return self.__cachedLinkedEntities

        try:
            if self.linked_files == None:
                return []
            
            files_list = self.linked_files.split(",")
            entities_ids = []
            files_ids = []
            for file_listed in files_list:
                file_listed_type = file_listed.split("_")
                if len(file_listed_type) < 1:
                    continue

                if file_listed_type[0] == "file":
                    files_ids.append(int(file_listed_type[1]))
                else:
                    entities_ids.append(int(file_listed_type[1]))

            linked_entities = self.get(entities_ids)
            linked_files    = File.get(files_ids)
            linked_array = []
            for _e in linked_entities:
                linked_array.append(_e)
            for _e in linked_files:
                linked_array.append(_e)

        except Exception as ____e:
            logger.logException(input_exception=____e,section="Entity",silent=False)
            return []
        
        self.__cachedLinkedEntities = linked_array
        return linked_array
    
    def getApiStructure(self, sensitive=False):
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
        if type(id) == int:
            try:
                return Entity.select().where(Entity.id == id).where(Entity.deleted == 0).get()
            except:
                return None
        else:
            try:
                __arr = []
                for _e in Entity.select().where(Entity.id << id).where(Entity.deleted == 0):
                    __arr.append(_e)

                return __arr
            except Exception as __egetexeption:
                #print(__egetexeption)
                return []

    @staticmethod
    def fromJson(json_input, passed_params):
        FINAL_ENTITY = Entity()
        if json_input.get("hash") == None:
            __hash = utils.getRandomHash(32)
        else:
            __hash = json_input.get("hash")
        
        indexation_content_ = json_input.get("indexation_content")
        internal_content_ = json_input.get("internal_content")

        # FINAL_ENTITY.hash = __hash
        if internal_content_ != None:
            FINAL_ENTITY.internal_content = json.dumps(internal_content_, ensure_ascii=False)
        else:
            try:
                internal_content_ = utils.clearJson(indexation_content_)
                FINAL_ENTITY.internal_content = json.dumps(internal_content_, ensure_ascii=False)
            except Exception:
                FINAL_ENTITY.internal_content = json.dumps(indexation_content_, ensure_ascii=False)
        if json_input.get("file") != None:
            FINAL_ENTITY.file_id = json_input.get("file").id
            FINAL_ENTITY.__cached_file = json_input.get("file")
        
        if json_input.get("unlisted", None) == True:
            FINAL_ENTITY.unlisted = 1

        if json_input.get("linked_files") != None:
            __out = []
            for item in json_input.get("linked_files"):
                if item == None:
                    continue
                
                __out.append(f"{item.self_name}_{item.id}")
            
            if len(__out) > 0:
                FINAL_ENTITY.linked_files = ",".join(__out)
                FINAL_ENTITY.__cachedLinkedEntities = json_input.get("linked_files")
        
        FINAL_ENTITY.extractor_name = json_input.get("extractor_name")
        if passed_params.get("display_name") != None:
            FINAL_ENTITY.display_name = passed_params["display_name"]
        else:
            if json_input.get("suggested_name") == None:
                if json_input.get("file") == None:
                    FINAL_ENTITY.display_name = "N/A"
                else:
                    FINAL_ENTITY.display_name = json_input.get("file").upload_name
            else:
                FINAL_ENTITY.display_name = json_input.get("suggested_name")
        
        if passed_params.get("description") != None:
            FINAL_ENTITY.description = passed_params["description"]
        if json_input.get("source") != None:
            FINAL_ENTITY.source = json_input.get("source")
        if json_input.get("declared_created_at") != None:
            FINAL_ENTITY.declared_created_at = int(json_input.get("declared_created_at"))
        if json_input.get("indexation_content") != None:
            #FINAL_ENTITY.indexation_content = json_input.dumps(indexation_content_) # remove
            FINAL_ENTITY.indexation_content_string = str(utils.json_values_to_string(indexation_content_)).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")
        else:
            FINAL_ENTITY.indexation_content_string = json.dumps(utils.json_values_to_string(internal_content_), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        return FINAL_ENTITY

    def saveInfoToJson(self, dir):
        with open(os.path.join(dir, f"data_{self.id}.json"), "w", encoding='utf8') as json_file:
            json_file.write(json.dumps(self.getApiStructure(sensitive=True), indent=2, ensure_ascii=False))
    
    async def export(self, export_dir, linked_params = {}, recursion = 0):
        if recursion > 5:
            return
        if export_dir.is_dir() == False:
            export_dir.mkdir()
        
        linked_dir = Path(os.path.join(str(export_dir), str(self.id) + "_linked"))         
        __file = self.file
        if __file != None and type(__file) != list:
            await __file.export(export_dir)

        if linked_params.get("export_linked", True) == True:
            linked_entities = self.getLinkedEntities()
            if linked_params.get("linked_to_main_dir", True) == True:
                linked_dir = export_dir

            if len(linked_entities) > 0:
                try:
                    if linked_dir.exists() == False:
                        linked_dir.mkdir()
                except FileExistsError:
                    pass

                for LINKED in linked_entities:
                    linked_entity_dir = Path(os.path.join(str(linked_dir), str(LINKED.id)))
                    if linked_params.get("linked_to_subdirs") == False:
                        linked_entity_dir = linked_dir

                    try:
                        if linked_entity_dir.exists() == False:
                            linked_entity_dir.mkdir()
                    except FileExistsError:
                        pass

                    if LINKED.self_name == "entity":
                        await LINKED.export(linked_entity_dir, {}, recursion + 1)
                    else:
                        await LINKED.export(linked_entity_dir)

                    logger.log(f"Exported {LINKED.self_name} {LINKED.id}", section="Export",name="success")

        logger.log(f"Exported entity {self.id}", section="Export",name="success")
        if linked_params.get("export_save_json_to_dir", True):
            self.saveInfoToJson(dir=str(export_dir))
