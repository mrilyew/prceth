from resources.Globals import consts, os, Path, utils, file_manager, zipfile, logger, json, shutil
from executables.acts.Base import BaseAct
from db.Collection import Collection
from peewee import Model, SqliteDatabase
from db.Entity import Entity
from db.Relation import Relation

class AImportQCL(BaseAct):
    name = 'AImportQCL'
    category = 'export'
    accepts = 'string'
    
    def execute(self, i: str, args):
        __IMPORT_PATH = i
        assert __IMPORT_PATH != None, "qcl path is not passed"
        IMPORT_PATH = Path(__IMPORT_PATH)
        if IMPORT_PATH.is_dir() or IMPORT_PATH.is_file() == False:
            raise Exception("invalid path")
        if IMPORT_PATH.suffix != ".qcl":
            raise Exception("not a qcl file")
        
        ___HASH = utils.getRandomHash(32)
        ___TEMP_UNPACK_DIR = args.get("temp_unpack_dir", os.path.join(consts["tmp"], "exports", ___HASH))
        TEMP_UNPACK_DIR = Path(___TEMP_UNPACK_DIR)
        TEMP_UNPACK_DIR.mkdir()

        logger.log(message="Extracting qcl",section="AImportQCL")
        with zipfile.ZipFile(__IMPORT_PATH, "r") as zip_ref: # Unzipping
            zip_ref.extractall(os.path.join(___TEMP_UNPACK_DIR))

        # ---- Making things

        ___UNPACKED_DB = os.path.join(___TEMP_UNPACK_DIR, "entities.db")
        ___UNPACKED_INFO = os.path.join(___TEMP_UNPACK_DIR, "INFO")
        ___UNPACKED_FILES = os.path.join(___TEMP_UNPACK_DIR, "entities")

        # Ok, recieving information.
        logger.log(message="Reading INFO",section="AImportQCL")

        __INFO_FILE = open(___UNPACKED_INFO, 'r', encoding='utf-8')
        __text_info_file = __INFO_FILE.read()
        __INFO_JSON = json.loads(__text_info_file)
        __INFO_FILE.close()
        # New collection.
        logger.log(message="Creating new collection",section="AImportQCL")

        ADD_AFTER = None
        ___coll = Collection()
        ___coll.name = __INFO_JSON.get("name")
        ___coll.description = __INFO_JSON.get("description")
        ___coll.tags = __INFO_JSON.get("tags")
        ___coll.author = __INFO_JSON.get("author")
        ___coll.source = __INFO_JSON.get("source")
        ___coll.frontend_data = __INFO_JSON.get("frontend_data")
        ___coll.order = Collection.getAllCount()
        if "to_add" in args:
            __add_collection = Collection.get(int(args.get("to_add")))
            if __add_collection != None:
                ADD_AFTER = __add_collection
            
        if ADD_AFTER != None:
            ___coll.unlisted = 1
        
        ___coll.save(force_insert=True)
        if ADD_AFTER != None:
            ADD_AFTER.addItem(___coll)
        
        # Appending entities.
        __DB = SqliteDatabase(___UNPACKED_DB)
        mk = []

        # Exporting entities to new DB
        with utils.overrideDb(Entity, __DB):
            __DB.connect()

            logger.log(message="Getting items",section="AImportQCL")

            for ITEM in Entity.fetchItems():
                ___ID = ITEM.hash

                __data = ITEM.__dict__["__data__"]
                __data.pop('id')
                mk.append(__data)

        __DB.close()

        for NEW_ITEM in mk:
            logger.log(message=f"Inserting Entity {NEW_ITEM.get("hash")}",section="AImportQCL")
            q = Entity.create(**NEW_ITEM)
            q.save()

            # Making relation
            rel = Relation()
            rel.parent_collection_id = ___coll.id
            rel.child_entity_id = q.id
            
            rel.save()

            if NEW_ITEM.get("type") != 1:
                HASH = NEW_ITEM.get("hash")
                MINI_HASH = HASH[0:2]
                NEW_MINI_HASH_DIR = os.path.join(consts["storage"], "collections", MINI_HASH)
                os.makedirs(NEW_MINI_HASH_DIR, exist_ok=True)

                __ITEM_FOLDER = os.path.join(___UNPACKED_FILES, HASH)
                __NEW_PATH = Path(os.path.join(NEW_MINI_HASH_DIR, HASH))
                if __NEW_PATH.is_dir():
                    logger.log(f"Didn't copied file {str(__ITEM_FOLDER)}", "AImportQCL", "error")
                    continue

                Path(__ITEM_FOLDER).rename(str(__NEW_PATH))
        
        file_manager.rmdir(str_path=___TEMP_UNPACK_DIR)

        return {
            "collection": ___coll.getApiStructure()
        }
