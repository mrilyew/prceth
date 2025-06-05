from resources.Consts import consts
from utils.MainUtils import replace_cwd, replace_src
from storage.StorageItem import StorageItem
from storage.TempStorage import TempStorage

class Storage:
    __items = {}

    def __init__(self, config):
        self.storage_dir = replace_src(replace_cwd(config.get("storage.root_path")))

        temp_storage = TempStorage(self.storage_dir, "temp")
        self.__items["tmp"] = temp_storage
        self.__items["tmp_files"] = temp_storage.subDir("files")
        self.__items["tmp_exports"] = temp_storage.subDir("exports")

        self.__items["settings"] = StorageItem(self.storage_dir, "settings")
        self.__items["files"] = StorageItem(self.storage_dir, "files")
        self.__items["binary"] = StorageItem(self.storage_dir, "binary")
        self.__items["logs"] = StorageItem(self.storage_dir, "logs")
        self.__items["dbs"] = StorageItem(self.storage_dir, "dbs")

    def sub(self, storage_name):
        return self.__items.get(storage_name)
