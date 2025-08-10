from executables.representations import Representation

class WebPage(Representation):
    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
