from utils.MainUtils import resolve_doc

class Argument:
    def __init__(self, data):
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
            for index, name in enumerate(__docs.get('values')):
                __val = __docs.get('values').get(name)

                __fnl['values'][name] = resolve_doc(__val)

        return __fnl

    def default(self):
        return self.data.get('default', None)

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
                assert got_value != None, f"{__name} not passed"

    def special_assert(self, inp):
        pass
