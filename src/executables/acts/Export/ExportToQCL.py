from resources.Globals import consts, os, Path, datetime, utils, logger, file_manager, zipfile, json
from executables.acts.Base import BaseAct
from peewee import Model, SqliteDatabase
from db.Entity import Entity
from db.Collection import Collection

class ExportToQCL(BaseAct):
    name = 'NOT WORKING BRO'
    category = 'export'
    accepts = 'collection'

    def execute(self, i: Collection, args):
        # Pathes

        __EXPORTS_PATH = os.path.join(consts["tmp"], "exports")
        __SAVE_PATH = args.get("save_path", __EXPORTS_PATH)
        __FILE_NAME = f"col{i.id}_{datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}"
        __FILE_EXT_NAME = __FILE_NAME + ".qcl"
        __SAVE_DIR_PATH = os.path.join(__EXPORTS_PATH, __FILE_NAME)
        __SAVE_STORAGE_PATH = os.path.join(__SAVE_DIR_PATH, "entities")
        __SAVE_FILE_PATH = os.path.join(__SAVE_PATH, __FILE_EXT_NAME)

        # Args

        __compression_level = args.get("compression", "ZIP_DEFLATED") # ZIP_STORED | ZIP_BZIP2 | ZIP_LZMA
        COMPRESSION = zipfile.ZIP_STORED
        match(__compression_level):
            case "ZIP_DEFLATED":
                COMPRESSION = zipfile.ZIP_DEFLATED
            case "ZIP_BZIP2":
                COMPRESSION = zipfile.ZIP_BZIP2
            case "ZIP_LZMA":
                COMPRESSION = zipfile.ZIP_LZMA
            case _:
                pass
        # Action

        logger.log(message="Making directories",section="ExportToQCL")

        SAVE_FILE_PATH = Path(__SAVE_DIR_PATH)
        SAVE_FILE_PATH.mkdir(exist_ok=True)

        SAVE_STORAGE_PATH = Path(__SAVE_STORAGE_PATH)
        SAVE_STORAGE_PATH.mkdir(exist_ok=True)

        DATABASE_PATH = os.path.join(__SAVE_DIR_PATH, "entities.db")

        __DB = SqliteDatabase(DATABASE_PATH)
        __ITEMS = i.getItems(offset=0,limit=None)

        # Exporting entities to new DB
        with utils.overrideDb(Entity, __DB):
            __DB.connect()
            __DB.create_tables([Entity], safe=True)

            logger.log(message="Created DB and entities table",section="ExportToQCL")

            for ITEM in __ITEMS:
                ___ID = ITEM.id
                ___TYPE = ITEM.type

                logger.log(message=f"Inserting Entity №{___ID}",section="ExportToQCL")
                
                __data = ITEM.__dict__["__data__"]
                __data.pop('id')
                ITEM.insert(__data).execute()
                
                if ___TYPE != 1:
                    logger.log(message=f"Copying Entity №{___ID} files",section="ExportToQCL")

                    HASH = ITEM.hash
                    __hash_path = os.path.join(__SAVE_STORAGE_PATH, HASH)
                    os.makedirs(__hash_path, exist_ok=True)

                    file_manager.copytree(src=ITEM.getDirPath(),dst=__hash_path)

        __DB.close()
        logger.log(message="Making \"INFO\" file",section="ExportToQCL")
        __RES__ = {
            "name": i.name,
            "description": i.description,
            "author": i.author,
            "source": i,
            "frontend_data": i.frontend_data,
            "tags": i.tags,
            "flags": i.flags,
        }

        __INFO_FILE = open(os.path.join(__SAVE_DIR_PATH, "INFO"), 'w', encoding='utf-8')
        json.dump(__RES__, __INFO_FILE)
        __INFO_FILE.close()

        logger.log(message="Copying table dir to zip",section="ExportToQCL")

        zf = zipfile.ZipFile(__SAVE_FILE_PATH, "w", compression=COMPRESSION)
        with zf as zip_file:
            for entry in SAVE_FILE_PATH.rglob("*"):
                zip_file.write(entry, entry.relative_to(SAVE_FILE_PATH))
        
        zf.close()

        logger.log(message="OK, removing original directory.",section="ExportToQCL")
        file_manager.rmdir(str_path=__SAVE_DIR_PATH)

        return {
            "destination": __SAVE_FILE_PATH
        }
