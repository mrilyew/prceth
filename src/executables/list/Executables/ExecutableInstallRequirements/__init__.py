from executables.acts import Act
from declarable.Arguments import ActArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["i"] = ActArgument({
            "assertion": {
                "not_null": True
            }
        })
        params["ignore_requirements"] = ActArgument({
            'default': False,
        })

        return params
