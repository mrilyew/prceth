from executables.thumbnail.Base import BaseThumbnail
from resources.Globals import Image, config, utils, os

class TImage(BaseThumbnail):
    name = 'TImage'
    accept = ["jpg", "png", "jpeg", "bmp", "gif", "tiff"]

    def run(self, file, params={}):
        size = (config.get("thumbnail.width"), config.get("thumbnail.height"))
        path = file.getPath()
        __previews = {
            "photo": []
        }

        if params.get("preview_file"):
            path = self.save_dir + "/" + params.get("preview_file")
        
        with Image.open(path) as img:
            __hash = utils.getRandomHash(8)

            img.thumbnail(size, Image.LANCZOS)
            new_img = Image.new('RGB', size, (0, 0, 0))

            img_width = (size[0] - img.size[0]) // 2
            img_height = (size[1] - img.size[1]) // 2
            new_img.paste(
                img, 
                (img_width, img_height)
            )

            __new_prev = os.path.join(self.save_dir, f"{__hash}_thumb.jpg")
            __previews["photo"].append({
                "path": f"{__hash}_thumb.jpg",
                "width": config.get("thumbnail.width"),
                "height": config.get("thumbnail.height")
            })

            new_img.save(__new_prev)
        
        return __previews
