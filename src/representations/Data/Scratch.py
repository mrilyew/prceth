from representations.Representation import Representation

class Scratch(Representation):
    category = "Data"

    async def extractByDefault(self, i = {}):
        out = self.new_cu({
            'content': {},
        })

        return [out]

    def extractWheel(self, i = {}):
        return 'extractByDefault'
