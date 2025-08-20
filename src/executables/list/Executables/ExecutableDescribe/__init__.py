from declarable.ArgumentsTypes import StringArgument, LimitedArgument
from executables.list.Executables.ExecutableList import Implementation as ListImplementation

class Implementation(ListImplementation):
    @classmethod
    def declare(cls):
        params = {}
        params["class"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        class_type = i.get('class_type')
        class_name = i.get('class')

        repo = self._classes[class_type]
        result = repo.findByName(class_name)

        assert result != None, "not found class"

        return result.describe()
