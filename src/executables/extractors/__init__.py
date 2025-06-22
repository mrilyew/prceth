from executables.Executable import Executable
from db.DbInsert import db_insert

class BaseExtractor(Executable):
    add_after = []
    linked_dict = None

    def link(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def collectionable(self, json_data: dict):
        coll_obj = db_insert.contentFromJson(json_data)
        coll_obj.is_collection = True

        coll_obj.save(force_insert=True)

        return coll_obj
