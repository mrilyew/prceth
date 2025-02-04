from resources.globals import consts, os, file_manager, Path

class AssetsCacheStorage():
    def __init__(self):
        self.path = consts["storage"] + "\\assets_originals"
        self.files = os.listdir(self.path)

    def contains(self, filename):
        return filename in self.files
    
    def append(self, filename):
        self.files.append(filename)

    def mklink_from_cache_to_dir(self, input_path):
        _path = Path(input_path)
        file_manager.symlinkFile(Path(self.path + "\\" + _path.name), _path)

assets_cache_storage = AssetsCacheStorage()
