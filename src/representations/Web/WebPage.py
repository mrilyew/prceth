from representations.Representation import Representation

class WebPage(Representation):
    common_category = "data"

    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
