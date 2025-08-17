from executables.representations import Representation

class WebPage(Representation):
    required_modules = ["selenium", "beautifulsoup4", "fake-useragent"]

    def extractByHtml(self, i = {}):
        xml_text = i.get('html')

    def extractByUrl(self, i = {}):
        url = i.get('url')
