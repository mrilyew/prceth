from utils.MainUtils import dump_json
from app.App import storage

class ThumbnailState:
    directory = None
    hash = None

    def new(self, hash):
        self.hash = hash
        self.directory = storage.sub('thumbnails').allocateHashOnce(self.hash)

    def get_dir(self):
        _dir = self.directory

        return _dir

    def write_data(self, data):
        self.data = data

    def serialize(self):
        return dump_json(self.data)
