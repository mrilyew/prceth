from resources.Globals import consts, BaseModel, Path
from peewee import TextField, IntegerField, BigIntegerField, AutoField, BooleanField, TimestampField

# File is not a file, its a directory with main file and secondary files.
# So the dir and main file names as hash
class File(BaseModel):
    self_name = 'file'
    temp_dir = ''

    id = AutoField() # Absolute id
    hash = TextField(null=True) # Entity hash
    upload_name = TextField(index=True,default='N/A') # Upload name (with extension)
    extension = TextField(null=True) # File extension
    filesize = BigIntegerField(default=0) # Size of file
    #dir_filesize = BigIntegerField(default=0) # Size of dir

    def move(self):
        from resources.Globals import storage

        __hash_dir = storage.makeHashDir(self.hash, only_return=True)
        Path(self.temp_dir).rename(__hash_dir)
        
        entity_file_path = Path(__hash_dir + '\\' + self.upload_name)
        entity_file_path_replace = f'{__hash_dir}\\{str((str(self.hash) + '.' + self.extension))}'
        entity_file_path.rename(entity_file_path_replace)
