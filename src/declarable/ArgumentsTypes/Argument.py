from resources.Consts import consts
from utils.MainUtils import resolve_lang

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

        return ps

    def passValue(self, val):
        self.input_value = val

    def manual(self):
        __lang_code = consts.get('ui.lang', 'eng')
        __fnl  = {}
        __docs = self.data.get('docs')

        if __docs == None:
            return {}

        if __docs.get('definition') != None:
            __fnl['definition'] = resolve_lang(__docs.get('definition'), __lang_code)

        if __docs.get('values') != None:
            __fnl['values'] = {}
            for index, name in enumerate(__docs.get('values')):
                __fnl['values'][name] = resolve_lang(__docs.get('values').get(name), __lang_code)

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
