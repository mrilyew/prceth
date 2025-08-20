from executables.list.Files.File import File
from executables.thumbnails.ImageMethod import ImageMethod
from PIL import Image as PILImage

class Implementation(File):
    docs = {
        "name": "representations.mime.image.name",
        "definition": "representations.mime.image.definition",
    }

    class Extractor(File.Extractor):
        async def process_item(self, item):
            new_data = {}
            common_link = item.common_link

            with PILImage.open(str(common_link.path())) as img:
                new_data = {
                    "width": img.size[0],
                    "height": img.size[1],
                }

            item.update_data(new_data)

            return item

    class Thumbnail(ImageMethod):
        pass
