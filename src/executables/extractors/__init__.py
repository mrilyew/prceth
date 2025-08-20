from executables.Executable import Executable

class Extractor(Executable):
    self_name = "Extractor"
    link_after = []
    linked_dict = None
    base_categories = ["template", "base", "extractors"]

    def subscribe(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def link_after_add(self, item):
        self.link_after.append(item)

    def self_insert(self, item):
        item.via_extractor = self

        return item
