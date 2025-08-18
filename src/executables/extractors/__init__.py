from executables.Executable import Executable

class BaseExtractor(Executable):
    add_after = []
    linked_dict = None
    base_categories = ["template", "base", "extractors"]

    def link(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def self_insert(self, item):
        item.via_extractor = self

        return item
