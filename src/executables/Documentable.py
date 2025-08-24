class Documentable():
    docs = {
        "definition": "no_description_defined",
    }

    @classmethod
    def describe(cls):
        module_name = cls.__module__.split('.')
        category = module_name[-2]
        name = module_name[-1]

        ts = {
            'category': category,
            'name': name,
            'docs': cls.docs,
            'args': [],
        }

        _args = cls.declare_recursive()
        for _name, _item in _args.items():
            _p = _args.get(_name).describe()

            _p['name'] = _name
            ts['args'].append(_p)

        if getattr(cls, "PreExecute", None) != None:
            pre_exec = cls.PreExecute

            ts["confirmation"] = pre_exec.args_list

        return ts
