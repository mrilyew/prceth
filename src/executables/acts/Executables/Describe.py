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
        class_full_name = class_object.__name__
        class_full_name_spl = class_full_name.split('.')
        section = class_full_name_spl[-3]
        category = class_full_name_spl[-2]
        name = class_full_name_spl[-1]

        ts = {
            'class_name': class_full_name,
            'sub': section,
            'category': category,
            'name': name,
            'args': {},
        }

        _args = self.declare_recursive()
        for _id, _name in enumerate(_args):
            ts['args'][_name] = _args.get(_name).out()

        return ts
