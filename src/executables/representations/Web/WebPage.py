from executables.representations import Representation

class WebPage(Representation):
    category = "Web"

    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
