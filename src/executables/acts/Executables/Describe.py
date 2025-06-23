from executables.acts import BaseAct
from declarable.ArgumentsTypes import StringArgument, LimitedArgument
from repositories.ExecutableRepository import ExecutableRepository

class Describe(BaseAct):
    category = 'Executables'

    @classmethod
    def declare(cls):
        params = {}
        params["class"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["class_type"] = LimitedArgument({
            "values": ['representation', 'extractor', 'act', 'service'],
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        class_type = i.get('class_type') + 's'
        class_name = i.get('class')

        class_object = ExecutableRepository().doImportRaw('executables', class_type, class_name)

        return class_object.describe()
