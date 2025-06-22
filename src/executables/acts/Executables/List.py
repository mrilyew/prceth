from executables.acts import BaseAct
from declarable.ArgumentsTypes import StringArgument, IntArgument

class List(BaseAct):
    category = 'Executables'

    @classmethod
    def declare(cls):
        params = {}
        params["class"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["display_name"] = StringArgument({})
        params["interval"] = IntArgument({
            "default": 60,
            "assertion": {
                "not_null": True,
            }
        })

        return params
