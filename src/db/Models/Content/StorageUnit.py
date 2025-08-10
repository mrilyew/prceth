import os, json
from app.App import logger, storage
from pathlib import Path
from peewee import TextField, BigIntegerField, IntegerField, BooleanField
from utils.MainUtils import extract_metadata_to_dict, get_random_hash
from db.Models.Content.ContentModel import BaseModel
from submodules.Files.FileManager import file_manager
import shutil, mimetypes

class StorageUnit(BaseModel):
    self_name = 'StorageUnit'
    short_name = 'su'
    temp_dir = None
    path_link = None

    class Meta:
        table_name = 'storage_units'

    # Identification
    uuid = IntegerField(unique=True, primary_key=True)
    hash = TextField(null=True)
    attached_path = TextField(null=True)

    upload_name = TextField(default='N/A') # Upload name (with extension)
    extension = TextField(default="json") # File extension
    mime = TextField(null=True,default="N/A")
    is_thumbnail = BooleanField(index=True,default=0)

    # Sizes
    filesize = BigIntegerField(default=0) # Size of main file
    dir_filesize = BigIntegerField(default=0) # Size of dir

    # Metadata
    metadata = TextField(default="")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.is_saved() == False:
            self.temp_dir = storage.sub('tmp_files').allocateTemp()

    def remove_temp(self):
        # get cursed
        if self.temp_dir != None:
            file_manager.rmdir(self.temp_dir)

    def generate_hash(self):
        self.hash = get_random_hash(32)

    def flush(self):
        self.save(force_insert=True)
        self.move_temp_dir()

    def set_mime(self):
        _mime = mimetypes.guess_type(self.path())
        self.mime = _mime[0]

    def set_dir_filesize(self):
        self.dir_filesize = file_manager.folder_size(self.temp_dir)

    def set_about(self):
        path = self.path_link

        file_stat = path.stat()
        self.filesize = file_stat.st_size
        self.extension = str(path.suffix[1:])
        self.upload_name = str(path.name)

    def set_main_file(self, path: Path):
        self.path_link = Path(path)
        self.generate_hash()
        self.set_about()
        self.set_mime()
        self.flush()

    def set_link(self, link):
        self.path_link = Path(link)
        self.link = str(link)

    def mark_as_preview(self):
        self.is_thumbnail = 1

    def write_data(self, json_data):
        self.extension = json_data.get("extension")

        if json_data.get("hash") == None:
            self.hash = get_random_hash(32)
        else:
            self.hash = json_data.get("hash")

        self.upload_name = json_data.get("upload_name")
        self.filesize = json_data.get("filesize")
        self.set_mime()
        self.set_dir_filesize()

        # broken function
        if json_data.get("link") != None:
            self.link = json_data.get("link")

        ''' TODO handle async
        if json_data.get("take_metadata", False) == True:
            self.fillMeta()'''

        if json_data.get('__flush__model__to__db__', True) == True:
            self.save(force_insert=True)

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

        file_name = (str(prefix) + str(self.upload_name))

        __list = os.listdir(current_dir_path)
        __count = len(__list)
        try:
            if __count > 0:
                shutil.copytree(str(current_dir_path), str(to_move_path), dirs_exist_ok = True)

                # renaming hashed filename to original
                Path(os.path.join(to_move_path, self.hash_filename())).rename(os.path.join(to_move_path, file_name))
        except Exception as __e__:
            logger.logException(__e__, "File", silent=False)

    async def export(self, dir_path, file_prefix = ""):
        self.save_to_dir(save_dir=dir_path, prefix=file_prefix)

    def api_structure(self):
        _ = {
            "id": self.uuid,
            "upload_name": self.upload_name,
            "extension": self.extension,
            "filesize": self.filesize,
            "dir_filesize": self.dir_filesize,
            "hash": self.hash,
            "upper_hash": str(self.upper_hash_dir()),
            "dir": str(self.dir_path()),
            "main_file": str(self.path()), 
        }
        _["relative_dir_path"] = self.relative_dir_path()
        _["relative_main_file_path"] = self.relative_main_file_path()

        return _

    def path(self):
        if getattr(self, "attached_path", None) != None:
            return self.attached_path

        __path = os.path.join(storage.sub('files').path(), self.hash[0:2])
        __end_dir = os.path.join(__path, self.hash)
        if self.temp_dir != None:
            __end_dir = self.temp_dir

        __path = os.path.join(__end_dir, str(self.hash_filename()))

        return Path(__path)

    def hash_filename(self):
        if self.temp_dir != None:
            return f"{self.upload_name}"

        return f"{self.hash}.{str(self.extension)}"

    def upper_hash_dir(self):
        return Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2])))

    def dir_path(self, need_check = False):
        __dir_path = Path(os.path.join(storage.sub('files').path(), str(self.hash[0:2]), self.hash))

        if need_check == True and __dir_path.exists() == False:
            __dir_path.mkdir(parents=True)

        return __dir_path

    def relative_dir_path(self):
        return f"{str(self.hash[0:2])}/{self.hash}"

    def relative_main_file_path(self):
        _p = self.relative_dir_path()

        return f"{_p}/{self.hash_filename()}"
