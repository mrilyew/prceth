from thumbnails.Thumbnail import Thumbnail
from thumbnails.ThumbnailState import ThumbnailState
from PIL import Image
from utils.MainUtils import get_random_hash
import os

class ImageThumbnail(Thumbnail):
    accepts = {
        'value': ['image/*']
    }

    def execute(self, i = {}):
        sizes = (i.get('width'), i.get('height'))

        previews = []
        path = i.get('path')

        with Image.open(path) as img:
            _state = ThumbnailState()
            _state.new(get_random_hash(12))

            img.thumbnail(sizes, Image.LANCZOS)

            new_img = Image.new('RGB', sizes, (0, 0, 0))

            img_width = (sizes[0] - img.size[0]) // 2
            img_height = (sizes[1] - img.size[1]) // 2

            new_img.paste(
                img, 
                (img_width, img_height)
            )

            _new_prev = os.path.join(_state.get_dir(), f"{_state.hash}.jpg")
            _state.write_data({
                'type': 'photo',
                'path': f"{_state.hash}\\{_state.hash}_thumb.jpg",
                'width': sizes[0],
                'height': sizes[1],
            })

            previews.append(_state)
            new_img.save(_new_prev)

        return previews
