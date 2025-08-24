from executables.list.Files.File import Implementation
from executables.thumbnails.ImageMethod import ImageMethod
from PIL import Image as PILImage

keys = {
    "image.name": {
        "en_US": "Image",
        "ru_RU": "Изображение"
    }
}

class Implementation(Implementation):
    docs = {
        "name": keys.get("image.name"),
    }
    inherit_submodules = True

    async def process_item(item):
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
