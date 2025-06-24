from executables.acts import BaseAct
from declarable.ArgumentsTypes import StringArgument, LimitedArgument
from repositories.ExecutableRepository import ExecutableRepository

class Describe(BaseAct):
    category = 'Executables'

    @classmethod
    def declare(cls):
        params = {}
        params["class_type"] = LimitedArgument({
            "values": ['representation', 'extractor', 'act', 'service'],
            "assertion": {
                "not_null": True,
            }
        })
        params["class"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        class_type = i.get('class_type')
        class_name = i.get('class')

        repo = ExecutableRepository()
        repo.part_name = class_type

        class_object = repo.doImport(class_name)

        return class_object.describe()
