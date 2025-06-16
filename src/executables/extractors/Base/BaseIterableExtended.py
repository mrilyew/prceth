from executables.extractors.Base.BaseTimeoutable import BaseTimeoutable
from declarable.ArgumentsTypes import IntArgument

class BaseIterableExtended(BaseTimeoutable):
    @classmethod
    def declare(cls):
        params = {}
        params["first_iteration"] = IntArgument({
            "default": 0
        })
        params["limit"] = IntArgument({
            "default": 0,
        })
        params["per_page"] = IntArgument({
            "default": 100
        })

        return params
