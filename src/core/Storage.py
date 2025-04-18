from resources.Globals import os, consts, Path, utils

class Storage:
    def __init__(self):
        self.storage_dir = consts["storage"]
        self.tmp_dir = consts["tmp"]
        self.tmp_coll_dir = os.path.join(self.tmp_dir, "files")
        if Path(self.tmp_dir).is_dir() == False:
            Path(self.tmp_dir).mkdir()

        if Path(self.tmp_coll_dir).is_dir() == False:
            Path(self.tmp_coll_dir).mkdir()

    def makeTemporaryCollectionDir(self, temp_dir_prefix = None):
        #rand = utils.random_int(1, 1000000) * -1
        if temp_dir_prefix == None:
            temp_dir_prefix = self.tmp_coll_dir
        
        rand = utils.getRandomHash(64)
        path = Path(os.path.join(temp_dir_prefix, str(rand)))
        path.mkdir(exist_ok=True)
        
        return str(path)

    def makeHashDir(self, hash, only_return = False):
        __hash_path = os.path.join(self.storage_dir, "files", hash[0:2])
        os.makedirs(__hash_path, exist_ok=True)
        __hash_path_dir = os.path.join(__hash_path, hash)
        if only_return == True:
            return __hash_path_dir

        os.makedirs(__hash_path_dir, exist_ok=True)

        return __hash_path_dir

storage = Storage()
