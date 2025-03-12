from executables.extractors.Base import BaseExtractor

class Template(BaseExtractor):
    name = 'template'
    category = 'template'
    
    def passParams(self, args):
        self.passed_params = args

        super().passParams(args)

    def onFail(self):
        pass

    async def run(self, args):
        pass

    async def postRun(self):
        pass
