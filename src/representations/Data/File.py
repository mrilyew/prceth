from representations.Representation import Representation

class File(Representation):
    common_category = "fs"

    def extractByPath(self, i = {}):
        path = i.get('path')

    def extractByContent(self, i = {}):
        text = i.get('text')
        original_name = i.get('original_name')
        extension = i.get('extension')

    def extractByUrl(self, i = {}):
        url = i.get('url')
