from db.Models.Content.ThumbnailState import ThumbnailState
from db.Models.Content.ContentModel import BaseModel
from executables.thumbnails import ThumbnailMethod
from PIL import Image as PILImage
from app.App import config
from pathlib import Path
import os

class ImageMethod(ThumbnailMethod):
    def create(self, item: BaseModel, params)->list:
        su = None
        if item.short_name == "su":
            su = item
        else:
            su = item.common_link

        sizes = (params.get('width', config.get("thumbnail.width")), params.get('height', config.get("thumbnail.height")))

        with PILImage.open(str(su.path())) as img:
            img.thumbnail(sizes, PILImage.LANCZOS)
            new_img = PILImage.new('RGB', sizes, (0, 0, 0))

            img_width = (sizes[0] - img.size[0]) // 2
            img_height = (sizes[1] - img.size[1]) // 2

            new_img.paste(
                img, 
                (img_width, img_height)
            )
            new_su = self.StorageUnit()
            new_prev = Path(os.path.join(new_su.temp_dir, f"{su.uuid}.jpg"))
            new_img.save(new_prev)

            new_su.mark_as_preview()
            new_su.set_main_file(new_prev)

            state = ThumbnailState({
                "type": "photo",
                "storage_unit_id": new_su.uuid,
                "width": img.size[0],
                "height": img.size[1],
            })

            return [state]
