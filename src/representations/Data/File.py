from representations.Representation import Representation

class File(Representation):
    category = "Data"

    def declare():
        params = {}
        params["path"] = {
            "type": "string",
            "default": None,
        }
        params["text"] = {
            "type": "string",
            "default": None,
        }
        params["url"] = {
            "type": "string",
            "default": None,
        }

        return params

    def extractWheel(self, i = {}):
        if 'path' in i:
            return 'extractByPath'
        elif 'text' in i:
            return 'extractByContent'
        elif 'url' in i:
            return 'extractByUrl'

    async def extractByPath(self, i = {}):
        path = i.get('path')

    async def extractByContent(self, i = {}):
        text = i.get('text')
        original_name = i.get('original_name')
        extension = i.get('extension')

    async def extractByUrl(self, i = {}):
        url = i.get('url')

    async def metadata(self, i = {}):
        return []
