import os, json
from resources.Consts import consts
from app.App import logger, storage
from pathlib import Path
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField
from utils.MainUtils import valid_name, extract_metadata_to_dict, get_random_hash
from db.BaseModel import BaseModel
from submodules.Files.FileManager import file_manager
import shutil

class StorageUnit(BaseModel):
    self_name = 'file'
    temp_dir = ''

    class Meta:
        table_name = 'storage_units'

    # Identification
    id = AutoField()
    hash = TextField(null=True)
    link = TextField(null=True,default=None)

    # Meta
    upload_name = TextField(default='N/A') # Upload name (with extension)
    extension = TextField(null=True,default="json") # File extension

    # Sizes
    filesize = BigIntegerField(default=0) # Size of main file
    dir_filesize = BigIntegerField(default=0) # Size of dir

    # Metadata
    metadata = TextField(null=True,default=None)

    def __init__(self):
        super().__init__()

        self.temp_dir = storage.sub('tmp_files').allocateTemp()

    def __del__(self):
        if self.temp_dir != None:
            file_manager.rmdir(self.temp_dir)

    def write_data(self, json_data):
        self.extension = json_data.get("extension")

        if json_data.get("hash") == None:
            self.hash = get_random_hash(32)
        else:
            self.hash = json_data.get("hash")

        self.upload_name = json_data.get("upload_name")
        self.filesize = json_data.get("filesize")

        if json_data.get("link") != None:
            self.link = json_data.get("link")
        
        # TODO handle async
        if json_data.get("take_metadata", False) == True:
            self.fillMeta()

        if json_data.get('__flush__model__to__db__', True) == True:
            self.save()

        self.move_temp_dir()

        if json_data.get('__move__from__temp__', True) == True:
            self.move_temp_dir()

    def move_temp_dir(self):
        '''
        Renames temp directory to new hash dir and changes main file name to hash
        '''
        if self.temp_dir == None:
            return 

        temp_dir = Path(self.temp_dir)

        current_path = Path(os.path.join(str(temp_dir), self.upload_name))
        new_name = Path(os.path.join(str(temp_dir), f"{'.'.join([str(self.hash), self.extension])}"))

        current_path.rename(str(new_name))

        new_storage_category = storage.sub('files').allocateHash(self.hash, only_return=True)
        temp_dir.rename(str(new_storage_category))
        
        self.temp_dir = None

    def save_to_dir(self, save_dir, prefix = ""):
        current_dir_path = self.dir_path()
        to_move_path = save_dir

        file_name = (prefix + str(self.upload_name)).replace("thumb", "th_umb") #быдлокод

        __list = os.listdir(current_dir_path)
        __count = len(__list)
        try:
            if __count > 0:
                shutil.copytree(str(current_dir_path), str(to_move_path), ignore=shutil.ignore_patterns('*_thumb.*'), dirs_exist_ok = True)
                
                # renaming hashed filename to original
                Path(os.path.join(to_move_path, self.hash_filename())).rename(os.path.join(to_move_path, file_name))
        except Exception as __e__:
            logger.logException(__e__, "File", silent=False)

    def api_structure(self):
        _ = {
            "id": self.id,
            "upload_name": self.upload_name,
            "extension": self.extension,
            "filesize": self.filesize,
            "hash": self.hash,
            "upper_hash": str(self.upper_hash_dir()),
            "dir": str(self.dir_path()),
            "main_file": str(self.path()), 
        }
        _["relative_path"] = f"{_.get('upper_hash')}/{_.get('hash')}"

        return _

    def path(self):
        if getattr(self, "link") != None:
            return self.link

        __path = os.path.join(storage.sub('files').path(), self.hash[0:2])
        __end_dir = os.path.join(__path, self.hash)
        if self.temp_dir != None:
            __end_dir = self.temp_dir

        __path = os.path.join(__end_dir, str(self.hash_filename()))

        return __path

    def hash_filename(self):
        return f"{self.hash}.{str(self.extension)}"

    def upper_hash_dir(self):
        return Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2])))

    def dir_path(self, need_check = False):
        __dir_path = Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2]), self.hash))

        if need_check == True and __dir_path.exists() == False:
            __dir_path.mkdir(parents=True)

        return __dir_path

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
