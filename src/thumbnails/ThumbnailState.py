from utils.MainUtils import dump_json
from app.App import storage

class ThumbnailState:
    tmp = None
    hash = None

    def new(self, hash):
        self.tmp = storage.sub('tmp').allocateTemp()
        self.hash = hash

    def get_dir(self):
        _dir = storage.sub('thumbnails').allocateHashOnce(self.hash)

        return _dir

    def write_data(self, data):
        self.data = data

    def serialize(self):
        return dump_json(self.data)
