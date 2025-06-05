from representations.Representation import Representation

class File(Representation):
    common_category = "fs"

    def extractWheel(self, i = {}):
        if 'path' in i:
            return 'extractByPath'
        elif 'text' in i:
            return 'extractByContent'
        elif 'url' in i:
            return 'extractByUrl'

    def extractByPath(self, i = {}):
        path = i.get('path')

    def extractByContent(self, i = {}):
        text = i.get('text')
        original_name = i.get('original_name')
        extension = i.get('extension')

    def extractByUrl(self, i = {}):
        url = i.get('url')

    def metadata(self, i = {}):
        return []
