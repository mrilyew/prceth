from representations.Representation import Representation

class Json(Representation):
    category = "Data"

    def extractByText(self, i = {}):
        json_text = i.get('text')

    def extractByObject(self, i = {}):
        json_object = i.get('object')
