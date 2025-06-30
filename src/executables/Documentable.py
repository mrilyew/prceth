from utils.MainUtils import resolve_lang
from resources.Consts import consts
from resources.Descriptions import descriptions

class Documentable():
    docs = {
        "name": descriptions.get("no_name_defined"),
        "definition": descriptions.get("no_description_defined"),
    }

    @classmethod
    def describe(cls):
        __lang_code = consts.get('ui.lang', 'eng')

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
            if __name != None:
                if type(__name) == str:
                    __name = descriptions.get(__name)
            if __definition != None:
                if type(__definition) == str:
                    __definition = descriptions.get(__definition)

            ts["docs"] = {
                "name": resolve_lang(__name, __lang_code),
                "definition": resolve_lang(__definition, __lang_code)
            }

        return ts
