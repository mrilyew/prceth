from executables.acts import Act
from declarable.Arguments import ExecutableArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["class"] = ExecutableArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        return i.get('class').describe()
