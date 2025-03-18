from executables.extractors.Base import BaseExtractor

class Template(BaseExtractor):
    name = 'template'
    category = 'template'
    
    def setArgs(self, args):
        self.passed_params = args

        super().setArgs(args)

    def onFail(self):
        pass

    async def run(self, args):
        pass

    async def postRun(self):
        pass
