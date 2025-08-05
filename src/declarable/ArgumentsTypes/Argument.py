from resources.Exceptions import InvalidArgumentName
from utils.MainUtils import resolve_doc
from resources.Consts import consts

class Argument:
    def __init__(self, data):
        if data.get('name') in consts.get('forbidden_argument_names'):
            raise InvalidArgumentName(f"{data.get('name')} is invalid argument name")

        self.data = data

    def out(self):
        ps = self.data.copy()
        ps.update({
            'type': self.__class__.__name__,
            'docs': self.manual()
        })

        if ps.get('sensitive') == True:
            ps['default'] = None
        else:
            ps['default'] = self.default()

        return ps

    def passValue(self, val):
        self.input_value = val

    def manual(self):
        __fnl  = {}
        __docs = self.data.get('docs')

        if __docs == None:
            return {}

        name = __docs.get('name')
        definition = __docs.get('definition')
        if name != None:
            __fnl['name'] = resolve_doc(name)

        if definition != None:
            __fnl['definition'] = resolve_doc(definition)

        if __docs.get('values') != None:
            __fnl['values'] = {}
            for index, name in enumerate(__docs.get("values")):
                __val = __docs.get('values').get(name)
                __name = __val.get("name")

                __fnl['values'][name] = {}
                __fnl['values'][name]["name"] = resolve_doc(__name)

        return __fnl

    def default(self):
        return self.data.get('default', None)

    def get(self, name, default = None):
        return self.data.get(name, default)

    def value(self):
        return self.input_value

    def val(self):
        #print(f"{self.data.get('name')}={self.input_value}={self.default()}")
        if self.input_value != None:
            return self.value()
        else:
            return self.default()

    def assertions(self, got_value):
        __assertion = self.data.get("assertion")
        __name = self.data.get('name')

        if __assertion != None:
            if __assertion.get("not_null") == True:
                assert got_value != None, f"{__name} is null"

    def special_assertions(self, inp):
        pass

    def conditions_assertions(self, all_args):
        __assertion = self.data.get("assertion")

        if __assertion != None:
            if __assertion.get("only_when") != None:
                only_when = __assertion.get("only_when")

                for condition in only_when:
                    _en = list(enumerate(condition))
                    key_name = _en[0][1]
                    key_value = condition.get(key_name)

                    operator = key_value.get("operator")

                    match(operator):
                        case "==":
                            assert all_args.get(key_name) == key_value.get("value"), f"{key_name} caused assertion"
                        case "!=":
                            assert all_args.get(key_name) != key_value.get("value"), f"{key_name} caused assertion"
