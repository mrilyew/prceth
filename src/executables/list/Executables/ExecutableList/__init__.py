from declarable.Arguments import LimitedArgument
from executables.acts import Act
from executables.representations import Representation
from executables.extractors import Extractor
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
        params["type"] = LimitedArgument({
            "values": ['representation', 'act', 'service'],
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def execute(self, i = {}):
        repo = self._classes[i.get("type")]
        lists = repo.findAll()
        fnl = []
        for item in lists:
            try:
                fnl.append(item.describe())
            except ModuleNotFoundError:
                pass
            except Exception as e:
                print(e)
                raise e

        return fnl
