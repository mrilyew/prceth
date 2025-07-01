from utils.MainUtils import resolve_doc

class Documentable():
    docs = {
        "name": "no_name_defined",
        "definition": "no_description_defined",
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
            'docs': {},
            'args': [],
        }

        docs = cls.docs
        _args = cls.declare_recursive()
        for _id, _name in enumerate(_args):
            _p = _args.get(_name).out()
            _p['name'] = _name
            ts['args'].append(_p)

        if docs != None:
            __name = docs.get('name')
            __definition = docs.get('definition')

            ts["docs"] = {
                "name": resolve_doc(__name),
                "definition": resolve_doc(__definition)
            }

        if cls.executable_cfg != None:
            variants = cls.executable_cfg.get('variants')

            if variants != None:
                ts['variants'] = []
                for variant in variants:
                    _var = variant.copy()
                    _var['name'] = resolve_doc(variant.get('name'))

                    ts['variants'].append(_var)

        return ts
