class Documentable():
    docs = {
        "name": {
            "en": "Not defined name"
        },
        "definition": {
            "en": "Not defined description"
        }
    }

    @classmethod
    def describe(cls):
        class_full_name = cls.__module__
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

        _args = cls.declare_recursive()
        for _id, _name in enumerate(_args):
            ts['args'][_name] = _args.get(_name).out()

        return ts
