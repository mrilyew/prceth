from db.Models.Content.StorageUnit import StorageUnit

# Pseudo model that represents thumbnail
class ThumbnailState():
    '''
    Format:

    "type" - "photo", "video"
    "storage_unit_id" - storage unit id
    "width" - width of preview
    "height" - same but height
    '''
    data = {}

    def __init__(self, json):
        self.write(json)

    def write(self, json):
        self.data = json

    def state(self):
        return self.data

    def api_structure(self):
        data = self.state()
        su = StorageUnit.ids(data.get("storage_unit_id"))

        if su:
            data["storage_unit"] = su.api_structure()

        return data
