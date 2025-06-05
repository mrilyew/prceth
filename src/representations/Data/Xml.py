from representations.Representation import Representation

class Xml(Representation):
    common_category = "data"

    def extractByText(self, i = {}):
        xml_text = i.get('text')
