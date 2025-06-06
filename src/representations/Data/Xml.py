from representations.Representation import Representation

class Xml(Representation):
    category = "Data"

    def extractByText(self, i = {}):
        xml_text = i.get('text')
