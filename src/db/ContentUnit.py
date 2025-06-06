import os, time, operator, utils, json5, json
from pathlib import Path
from submodules.Files.FileManager import file_manager
from app.App import logger
from resources.Consts import consts
from peewee import Model, TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField, JOIN
from db.StorageUnit import StorageUnit
from functools import reduce

class ContentUnit(Model):
    '''
    Model that represents unit of information.

    Fields:
    id: id of ContentUnit
    internal_content: json content of ContentUnit
    display_name: visual name of ContentUnit

    Methods:

    '''
    self_name = 'ContentUnit'
    __cached_file = None
    __cachedLinkedEntities = None

    # Identification
    id = AutoField() # Absolute id
    hash = TextField(null=True)

    # Data
    internal_content = TextField(null=True,default=None) # JSON data
    representation = TextField(null=True,default='base')
    extractor_name = TextField(null=True,default=None) # Extractor that was used for creation
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
    file_id = IntegerField(null=True) # File id
    linked_files = TextField(null=True) # Files list

    # Visibility
    unlisted = BooleanField(index=True,default=0)
    deleted = BooleanField(index=True,default=0)

    @property
    def file(self):
        if self.file_id == None:
            return None

        if self.__cached_file != None:
            return self.__cached_file

        _fl = File.get(self.file_id)
        self.__cached_file = _fl
        
        return _fl

    def delete(self):
        super().delete()

    def getFormattedInfo(self, recursive = False, recurse_level = 0):
        internal_content = getattr(self, "internal_content", "{}")
        if internal_content == None:
            internal_content = "{}"
        
        lods_ = json5.loads(internal_content)
        if recursive == True and recurse_level < 3:
            linked_files = self.getLinkedEntities()
            lods_ = utils.replace_strings_in_dicts(input_data=lods_,link_to_linked_files=linked_files,recurse_level=recurse_level)

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
            logger.logException(input_exception=____e,section="ContentUnit",silent=False)
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
        items = (ContentUnit.select()
                 .where(ContentUnit.unlisted == 0)
                 .where(ContentUnit.deleted == 0)
                 .join(File, on=(File.id == ContentUnit.file_id), join_type=JOIN.LEFT_OUTER))

        conditions = []

        for column in columns_search:
            match column:
                case "upload_name":
                    conditions.append((File.upload_name.contains(query)))
                case "display_name":
                    conditions.append((ContentUnit.display_name.contains(query)))
                case "description":
                    conditions.append((ContentUnit.description.contains(query)))
                case "source":
                    conditions.append((ContentUnit.source.contains(query)))
                case "index":
                    conditions.append((ContentUnit.indexation_content_string.contains(query)))
                case "saved":
                    conditions.append((ContentUnit.extractor_name.contains(query)))
                case "author":
                    conditions.append((ContentUnit.author.contains(query)))

        if conditions:
            items = items.where(reduce(operator.or_, conditions))

        return items
    
    @staticmethod
    def get(id):
        if type(id) == int:
            try:
                return ContentUnit.select().where(ContentUnit.id == id).where(ContentUnit.deleted == 0).get()
            except:
                return None
        else:
            try:
                __arr = []
                for _e in ContentUnit.select().where(ContentUnit.id << id).where(ContentUnit.deleted == 0):
                    __arr.append(_e)

                return __arr
            except Exception as __egetexeption:
                return []

    @staticmethod
    def fromJson(json_input, passed_params):
        FINAL_ContentUnit = ContentUnit()
        if json_input.get("hash") == None:
            __hash = utils.get_random_hash(32)
        else:
            __hash = json_input.get("hash")
        
        indexation_content_ = json_input.get("indexation_content")
        internal_content_ = json_input.get("internal_content")

        # FINAL_ContentUnit.hash = __hash
        if internal_content_ != None:
            FINAL_ContentUnit.internal_content = json.dumps(internal_content_, ensure_ascii=False)
        else:
            try:
                internal_content_ = utils.clear_json(indexation_content_)
                FINAL_ContentUnit.internal_content = json.dumps(internal_content_, ensure_ascii=False)
            except Exception:
                FINAL_ContentUnit.internal_content = json.dumps(indexation_content_, ensure_ascii=False)
        if json_input.get("file") != None:
            FINAL_ContentUnit.file_id = json_input.get("file").id
            FINAL_ContentUnit.__cached_file = json_input.get("file")
        
        if json_input.get("unlisted", None) == True:
            FINAL_ContentUnit.unlisted = 1

        if json_input.get("linked_files") != None:
            __out = []
            for item in json_input.get("linked_files"):
                if item == None:
                    continue
                
                __out.append(f"{item.self_name}_{item.id}")
            
            if len(__out) > 0:
                FINAL_ContentUnit.linked_files = ",".join(__out)
                FINAL_ContentUnit.__cachedLinkedEntities = json_input.get("linked_files")
        
        FINAL_ContentUnit.extractor_name = json_input.get("extractor_name")
        if passed_params.get("display_name") != None:
            FINAL_ContentUnit.display_name = passed_params["display_name"]
        else:
            if json_input.get("suggested_name") == None:
                if json_input.get("file") == None:
                    FINAL_ContentUnit.display_name = "N/A"
                else:
                    FINAL_ContentUnit.display_name = json_input.get("file").upload_name
            else:
                FINAL_ContentUnit.display_name = json_input.get("suggested_name")
        
        if passed_params.get("description") != None:
            FINAL_ContentUnit.description = passed_params["description"]
        if json_input.get("source") != None:
            FINAL_ContentUnit.source = json_input.get("source")
        if json_input.get("declared_created_at") != None:
            FINAL_ContentUnit.declared_created_at = int(json_input.get("declared_created_at"))
        if json_input.get("indexation_content") != None:
            #FINAL_ContentUnit.indexation_content = json_input.dumps(indexation_content_) # remove
            FINAL_ContentUnit.indexation_content_string = str(utils.json_values_to_string(indexation_content_)).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")
        else:
            FINAL_ContentUnit.indexation_content_string = json.dumps(utils.json_values_to_string(internal_content_), ensure_ascii=False).replace('None', '').replace('  ', ' ').replace('\n', ' ').replace(" ", "")

        return FINAL_ContentUnit

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
                    linked_ContentUnit_dir = Path(os.path.join(str(linked_dir), str(LINKED.id)))
                    if linked_params.get("linked_to_subdirs") == False:
                        linked_ContentUnit_dir = linked_dir

                    try:
                        if linked_ContentUnit_dir.exists() == False:
                            linked_ContentUnit_dir.mkdir()
                    except FileExistsError:
                        pass

                    if LINKED.self_name == "ContentUnit":
                        await LINKED.export(linked_ContentUnit_dir, {}, recursion + 1)
                    else:
                        await LINKED.export(linked_ContentUnit_dir)

                    logger.log(f"Exported {LINKED.self_name} {LINKED.id}", section="Export",name="success")

        logger.log(f"Exported ContentUnit {self.id}", section="Export",name="success")
        if linked_params.get("export_save_json_to_dir", True):
            self.saveInfoToJson(dir=str(export_dir))
