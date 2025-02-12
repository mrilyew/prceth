from executables.thumbnail.Base import BaseThumbnail
from resources.Globals import Image

class TImage(BaseThumbnail):
    name = 'TImage'
    accept = ["jpg", "png", "jpeg", "bmp", "gif", "tiff"]

    def run(self, entity, params={}):
        size = (200, 200)
        path = entity.getPath()
        if "another_file" in params:
            path = entity.getDirPath() + "/" + params.get("another_file")
        
        with Image.open(path) as img:
            img.thumbnail(size, Image.LANCZOS)
            new_img = Image.new('RGB', size, (0, 0, 0))
            new_img.paste(
                img, 
                ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
            )
            new_img.save(entity.getDirPath() + "/thumbnail_photo_0.jpg")
        
        return {
            "previews": "photo_0"
        }
