from resources.Globals import os, logger, asyncio, consts, datetime, zipfile, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Collection import Collection
from db.Entity import Entity
from db.File import File
from peewee import Model, SqliteDatabase

class ExportToZIP(BaseAct):
    name = 'ExportToZIP'
    category = 'export'
    accepts = 'collection'
    docs = {
        "description": {
            "name": {
                "ru": "Экспорт в ZIP",
                "en": "Export to ZIP"
            },
            "definition": {
                "ru": "Копирует содержимое коллекции в zip",
                "en": "Copies collection content to zip"
            }
        }
    }

    def declare():
        params = {}
        params["dir"] = {
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["compression"] = {
            "type": "array",
            "values": ["ZIP_LZMA", "ZIP_BZIP2", "ZIP_DEFLATED"],
            "default": "ZIP_DEFLATED"
        }
        params["pack_to_zip"] = {
            "type": "bool",
            "default": True,
        }
        return params

    async def execute(self, i: Collection, args = {}):
        __EXPORTS_TEMP_PATH = os.path.join(consts.get("tmp"), "exports")
        __SAVE_PATH = self.passed_params.get("dir", __EXPORTS_TEMP_PATH)
        __FILE_NAME = f"col{i.id}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
        __FILE_EXT_NAME = __FILE_NAME + ".zips",
        
        __SAVE_DIR_PATH = os.path.join(__EXPORTS_TEMP_PATH, __FILE_NAME)
        __SAVE_STORAGE_PATH = os.path.join(__SAVE_DIR_PATH, "entities")
        __SAVE_FILE_PATH = os.path.join(__SAVE_PATH, __FILE_EXT_NAME)

        # Args
        __compression_level = self.passed_params.get("compression", "ZIP_DEFLATED")
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
        logger.log(message="Making directories",section="Export")
        
        SAVE_FILE_PATH = Path(__SAVE_DIR_PATH)
        SAVE_FILE_PATH.mkdir(exist_ok=True)

        SAVE_STORAGE_PATH = Path(__SAVE_STORAGE_PATH)
        SAVE_STORAGE_PATH.mkdir(exist_ok=True)

        DATABASE_PATH = os.path.join(__SAVE_DIR_PATH, "entities.db")

        # DB Things
        __DB = SqliteDatabase(DATABASE_PATH)
        __ITEMS = i.getItems(offset=0,limit=None)

        with utils.overrideDb([Entity, File], __DB):
            __DB.connect()
            __DB.create_tables([Entity, File], safe=True)

            logger.log(message="Created DB and entities table",section="Export")

            for ITEM in __ITEMS:
                ___ID = ITEM.id

                logger.log(message=f"Inserting Entity №{___ID}",section="Export")
                
                __data = ITEM.__dict__["__data__"]
                __data.pop('id')
                ITEM.insert(__data).execute()

                # TODO: Linked
                logger.log(message=f"Copying Entity №{___ID} files",section="Export")
                '''
                HASH = ITEM.hash
                __hash_path = os.path.join(__SAVE_STORAGE_PATH, HASH)
                os.makedirs(__hash_path, exist_ok=True)

                file_manager.copytree(src=ITEM.getDirPath(),dst=__hash_path)'''

        __DB.close()

        logger.log(message="Making \"INFO\" file",section="Export")

        __RES__ = {
            "name": i.name,
            "description": i.description,
            "author": i.author,
            "source": i.source,
            "frontend_data": i.frontend_data,
            "tags": i.tags,
            #"flags": i.flags,
        }

        __INFO_FILE = open(os.path.join(__SAVE_DIR_PATH, "INFO"), 'w', encoding='utf-8')
        json.dump(__RES__, __INFO_FILE)
        __INFO_FILE.close()

        logger.log(message="Copying table dir to zip",section="Export")

        if self.passed_params.get("pack_to_zip") == True:
            zf = zipfile.ZipFile(__SAVE_FILE_PATH, "w", compression=COMPRESSION)
            with zf as zip_file:
                for entry in SAVE_FILE_PATH.rglob("*"):
                    zip_file.write(entry, entry.relative_to(SAVE_FILE_PATH))

            zf.close()

            logger.log(message="OK, removing original directory.",section="Export")
            file_manager.rmdir(str_path=__SAVE_DIR_PATH)

            return {
                "destination": __SAVE_FILE_PATH
            }

        return {
            "destination": __SAVE_DIR_PATH
        }
