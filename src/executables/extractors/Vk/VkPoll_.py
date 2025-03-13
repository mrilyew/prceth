from executables.extractors.Base import BaseExtractor

class VkPoll(BaseExtractor):
    name = 'VkPoll'
    category = 'Vk'
    
    def passParams(self, args):
        self.passed_params = args

        super().passParams(args)
    
    async def run(self, args):
        pass
