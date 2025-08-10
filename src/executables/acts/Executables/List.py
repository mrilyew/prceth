from executables.acts import BaseAct
from declarable.ArgumentsTypes import LimitedArgument
from repositories.ExecutableRepository import ExecutableRepository

class List(BaseAct):
    @classmethod
    def declare(cls):
        params = {}
        params["class_type"] = LimitedArgument({
            "values": ['representation', 'extractor', 'act', 'service'],
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        class_type = i.get('class_type')

        repo = ExecutableRepository()
        repo.part_name = class_type

        lists = repo.getList(class_type)
        fnl = []

        for item in lists:
            fnl.append(item.describe())

        return fnl
