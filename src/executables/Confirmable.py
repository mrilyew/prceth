class Confirmable():
    class PreExecute():
        args_list = []

        def __init__(self, outer):
            self.outer = outer
            self.outer_args = outer.declare_recursive()

        async def execute(self, i = {})->list:
            '''
            Should return list with argument classes
            '''
            return {
                "args": [],
                "data": {},
            }
