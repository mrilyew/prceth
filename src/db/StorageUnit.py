import os, json
from resources.Consts import consts
from app.App import logger
from pathlib import Path
from peewee import Model, TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField
from utils.MainUtils import valid_name, extract_metadata_to_dict
import shutil

class StorageUnit(Model):
    self_name = 'file'
    temp_dir = ''

    class Meta:
        table_name = 'storage_units'

    # Identification
    id = AutoField()
    hash = TextField(null=True)
    link = TextField(null=True,default=None)

    # Meta
    upload_name = TextField(index=True,default='N/A') # Upload name (with extension)
    extension = TextField(null=True,default="json") # File extension

    # Sizes
    filesize = BigIntegerField(default=0) # Size of main file
    dir_filesize = BigIntegerField(default=0) # Size of dir

    # Metadata
    metadata = TextField(null=True,default=None)

    def moveTempDir(self, use_upload_name = False, preset_dir = None, move_type = -1, append_ContentUnit_id_to_start = True):
        from app.App import storage
        
        TMP_DIR = self.temp_dir
        if TMP_DIR == None:
            return
        
        #self.temp_dir = None
        # Renaming main file 
        MAIN_FILE_PATH = Path(TMP_DIR + '\\' + self.upload_name)
        MAIN_FILE_PATH_NEW = f"{TMP_DIR}\\{str((str(self.hash) + '.' + self.extension))}"
        if use_upload_name != False:
            MAIN_FILE_PATH_NEW = f'{TMP_DIR}\\{str(self.upload_name)}.{str(self.extension)}'
        
        MAIN_FILE_PATH.rename(MAIN_FILE_PATH_NEW)
        
        # Making short hash directory
        # And returning full hash directory.
        FULL_HASH_DIRECTORY = None
        if preset_dir != None:
            if move_type == -10:
                FULL_HASH_DIRECTORY = Path(preset_dir)
            elif move_type == 0:
                FULL_HASH_DIRECTORY = Path(os.path.join(preset_dir, str(self.id)))
                Path(TMP_DIR).rename(FULL_HASH_DIRECTORY)
            elif move_type == 1:
                FULL_HASH_DIRECTORY = Path(TMP_DIR)
                __list = os.listdir(FULL_HASH_DIRECTORY)
                try:
                    if len(__list) < 1:
                        pass
                    elif len(__list) == 1:
                        new_name_unsafe = str(self.upload_name)
                        if append_ContentUnit_id_to_start == True:
                            new_name_unsafe = str(self.id) + "_" + new_name_unsafe
                        
                        new_name = valid_name(new_name_unsafe)
                        file_path = os.path.join(TMP_DIR, __list[0])

                        if os.path.isfile(file_path):
                            shutil.move(file_path, os.path.join(preset_dir, new_name))
                    elif len(__list) > 1:
                        FULL_HASH_DIRECTORY = Path(os.path.join(preset_dir, str(self.id)))
                        Path(TMP_DIR).rename(FULL_HASH_DIRECTORY)
                except Exception as __e__:
                    logger.logException(__e__, "File")
        else:
            FULL_HASH_DIRECTORY = Path(storage.makeHashDir(self.hash, only_return=True))
            Path(TMP_DIR).rename(FULL_HASH_DIRECTORY)

    def saveToDir(self, save_dir, prefix = ""):
        from app.App import storage

        CURRENT_FILE_PATH = Path(self.getDirPath())
        OUTPUT_FILE_PATH = save_dir

        NEW_MAIN_FILE_NAME = str(self.upload_name)
        NEW_MAIN_FILE_NAME = prefix + NEW_MAIN_FILE_NAME
        
        NEW_MAIN_FILE_NAME = NEW_MAIN_FILE_NAME.replace("thumb", "th_umb") #БЫДЛОКОД
        __list = os.listdir(CURRENT_FILE_PATH)
        __count = len(__list)
        FILES_LENGTH = __count
        try:
            if FILES_LENGTH > 0:
                shutil.copytree(str(CURRENT_FILE_PATH), str(OUTPUT_FILE_PATH), ignore=ignore_patterns('*_thumb.*'), dirs_exist_ok = True)
                Path(os.path.join(OUTPUT_FILE_PATH, self.getFsFileName())).rename(os.path.join(OUTPUT_FILE_PATH, NEW_MAIN_FILE_NAME))
        except Exception as __e__:
            logger.logException(__e__, "File")

    def api_structure(self):
        _ = {
            "extension": self.extension,
            "id": self.id,
            "upload_name": self.upload_name,
            "filesize": self.filesize,
            "dir": self.getDirPath(),
            "main_file": self.getPath(), 
            "hash": self.hash,
            "upper_hash": self.getUpperHashDirPath(),
        }
        _["relative_path"] = f"{_.get('upper_hash')}/{_.get('hash')}"

        return _

    @staticmethod
    def get(id):
        if type(id) == int:
            try:
                return File.select().where(File.id == id).get()
            except:
                return None
        else:
            try:
                __arr = []
                for _e in File.select().where(File.id << id):
                    __arr.append(_e)

                return __arr
            except Exception as __egetexeption:
                return []

    def path(self):
        STORAGE_PATH = consts["storage"]
        HASH = self.hash
        if getattr(self, "link") != None:
            return self.link

        COLLECTION_PATH = os.path.join(STORAGE_PATH, "files", HASH[0:2])
        END_DIR = os.path.join(COLLECTION_PATH, HASH)
        if self.temp_dir != None:
            END_DIR = self.temp_dir

        ContentUnit_PATH = os.path.join(END_DIR, str(self.upload_name))

        return ContentUnit_PATH

    def hash_filename(self):
        HASH = self.hash

        return f"{HASH}.{str(self.extension)}"

    def upper_hash_dir(self):
        STORAGE_PATH = consts["storage"]
        HASH = self.hash

        COLLECTION_PATH = os.path.join(STORAGE_PATH, "files", str(HASH[0:2]))
        COLLECTION_PATH_OBJ = Path(COLLECTION_PATH)

        return COLLECTION_PATH

    def dir_path(self, need_check = False):
        STORAGE_PATH = consts["storage"]
        HASH = self.hash

        COLLECTION_PATH = os.path.join(STORAGE_PATH, "files", str(HASH[0:2]), HASH)
        COLLECTION_PATH_OBJ = Path(COLLECTION_PATH)

        if need_check == True and COLLECTION_PATH_OBJ.exists() == False:
            COLLECTION_PATH_OBJ.mkdir(parents=True, exist_ok=True)

        return COLLECTION_PATH

    def fillMeta(self):
        from repositories.ActsRepository import ActsRepository

        metadata_act = (ActsRepository().getByName("Metadata.ExtractMetadata"))()
        ext_metadata_act = (ActsRepository().getByName("Metadata.AdditionalMetadata"))()
        metadata_act.setArgs()

        metadata_arr = metadata_act.execute(i=self)
        ext_metadata_arr = ext_metadata_act.execute(i=self)

        main_metadata = extract_metadata_to_dict(metadata_arr)
        main_metadata.update(ext_metadata_arr)

        self.metadata = json.dumps(main_metadata)

    async def export(self, dir, prefix = ""):
        self.saveToDir(save_dir=dir,prefix=prefix)
