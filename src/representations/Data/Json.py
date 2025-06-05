from representations.Representation import Representation

class Json(Representation):
    common_category = "data"

    def extractByText(self, i = {}):
        json_text = i.get('text')

    def extractByObject(self, i = {}):
        json_object = i.get('object')
