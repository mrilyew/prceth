from executables.Executable import Executable

class BaseExtractor(Executable):
    collections_add_after = []
    linked_dict = None

    def declare():
        params = {}
        params["display_name"] = {
            "name": "display_name",
            "type": "string",
            "default": None,
        }
        params["description"] = {
            "name": "description",
            "type": "string",
            "default": None,
        }
        params["unlisted"] = {
            "name": "unlisted",
            "type": "bool",
            "default": False,
        }

        return params

    def link(self, linked_dict: dict):
        self.linked_dict = linked_dict
