from declarable.Arguments import FloatArgument

class BaseTimeoutable:
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
