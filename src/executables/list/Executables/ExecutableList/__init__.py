from executables.acts import Act
from declarable.Arguments import LimitedArgument
from executables.representations import Representation
from executables.extractors import Extractor
from executables.acts import Act
from executables.services import Service

class Implementation(Act):
    _classes = {
        "representation": Representation,
        "extractor": Extractor,
        "act": Act,
        "service": Service,
    }

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

        repo = self._classes[class_type]
        lists = repo.getList()
        fnl = []

        for item in lists:
            fnl.append(item.describe())

        return fnl
