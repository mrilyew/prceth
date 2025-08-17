from utils.MainUtils import get_random_hash, override_db
from db.Models.Content.ContentModel import BaseModel
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from db.Models.Content.StorageUnit import StorageUnit
from peewee import Model, SqliteDatabase
from db.LinkManager import link_manager
from app.App import storage

class ArchiveExport:
    EXTENSION_NAME = "th"

    @classmethod
    def create_manager(cls):
        return ArchiveExport()

    def define_temp(self):
        _storage = storage.sub("tmp_exports")
        storage_path = _storage.path()

        self.tmp_path = storage_path.joinpath(get_random_hash(32))
        self.tmp_path.mkdir()

        self.content_path = self.tmp_path.joinpath("content")
        self.content_path.mkdir()

        # self.cu_path = self.content_path.joinpath("content_units")
        # self.cu_path.mkdir()

        self.su_path = self.content_path.joinpath("storage_units")
        self.su_path.mkdir()

    def define_db(self):
        self.db = SqliteDatabase(self.tmp_path.joinpath("items.db"))
        _models = [ContentUnit, StorageUnit, ContentUnitRelation]

        with override_db(_models, self.db):
            self.db.connect()
            self.db.create_tables(_models, safe=True)

    def end(self):
        self.db.close()

    def getByTypeAndId(self, type: str, id: int):
        element_class = None

        match(type):
            case "cu":
                element_class = ContentUnit.ids(int(id))
            case "su":
                element_class = StorageUnit.ids(int(id))

        return element_class

    async def export(self, item: BaseModel, args: dict):
        item_type = item.short_name
        save_at_db = True
        save_files = True

        if save_at_db == True:
            with override_db([ContentUnit, StorageUnit], self.db):
                item_data = item.__dict__["__data__"]
                item.insert(item_data).execute()

        match (item_type):
            case "su":
                pass
