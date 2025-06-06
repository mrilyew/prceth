from representations.Representation import Representation

class Scratch(Representation):
    category = "Data"

    async def extractByDefault(self, i = {}):
        out = self.new_cu({
            "source": {
                'type': 'api',
                'content': 'null',
            },
            'content': {},
        })

        return [out]

    def extractWheel(self, i = {}):
        return 'extractByDefault'
