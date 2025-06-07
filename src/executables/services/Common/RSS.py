from executables.services.Base.Base import BaseService

class RSS(BaseService):
    category = 'Common'
    c_cached_executable = None
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, i = {}):
        pass
