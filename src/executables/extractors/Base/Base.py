from executables.Executable import Executable
from representations.Data.Json import Json as JsonRepresentation

class BaseExtractor(Executable):
    add_after = []
    linked_dict = None

    def link(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def collectionable(self, json_data: dict):
        coll_obj = self.new_cu(json_data)
        coll_obj.is_collection = True

        coll_obj.save()

        return coll_obj
