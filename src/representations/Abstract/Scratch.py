from representations.Representation import Representation

class Scratch(Representation):
    category = "Abstract"

    async def extractByDefault(self, i = {}):
        out = self.new_cu({
            'content': i,
        })

        return [out]

    def extractWheel(self, i = {}):
        return 'extractByDefault'
