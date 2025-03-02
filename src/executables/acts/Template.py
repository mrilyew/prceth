from executables.acts.Base import BaseAct

class Template(BaseAct):
    name = 'ATemplate'
    category = 'base'
    accepts = 'entity'
    
    def execute(self, i, args):
        return {}
