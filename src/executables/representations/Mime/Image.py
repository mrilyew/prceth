from executables.representations.Data.File import File
from executables.thumbnails.ImageMethod import ImageMethod
from PIL import Image as PILImage

class Image(File):
    category = "Mime"

    class Extractor(File.Extractor):
        async def process_item(self, item):
            new_data = {}
            su = item.main_su

            with PILImage.open(str(su.path())) as img:
                new_data = {
                    "width": img.size[0],
                    "height": img.size[1],
                }

            item.update_data(new_data)

            return item

    class Thumbnail(ImageMethod):
        pass
