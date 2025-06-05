from pathlib import Path
import os

class StorageItem:
    def __init__(self, storage_root: str, storage_folder: str = None):
        self.root = storage_root
        self.dir = Path(os.path.join(storage_root, storage_folder))

        make_dir = True

        if make_dir == True and self.dir.is_dir() == False:
            self.dir.mkdir()

    def subDir(self, dir: str):
        return StorageItem(self.root, "/".join([str(self.dir), dir]))

    def allocateHash(self, hash, only_return = False):
        __main_hash_path = os.path.join(self.storage_dir, "files", hash[0:2])
        os.makedirs(__main_hash_path, exist_ok=True)

        __hash_path = os.path.join(__main_hash_path, hash)
        os.makedirs(__hash_path, exist_ok=True)

        return __hash_path

    def path(self):
        return self.dir
