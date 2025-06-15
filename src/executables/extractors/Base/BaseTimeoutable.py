from executables.extractors.Base.Base import BaseExtractor
from declarable.ArgumentsTypes import FloatArgument

class BaseTimeoutable(BaseExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["timeout"] = FloatArgument({
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        })

        return params