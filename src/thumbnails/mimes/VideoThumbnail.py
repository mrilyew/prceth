from thumbnails.Thumbnail import Thumbnail
from thumbnails.ThumbnailState import ThumbnailState
from utils.MainUtils import get_random_hash
from PIL import Image
from moviepy import VideoFileClip
from declarable.ArgumentsTypes import IntArgument
import os

class VideoThumbnail(Thumbnail):
    accepts = {
        'value': ['video/*']
    }

    def declare():
        params = {}
        params['frames'] = IntArgument({
            'default': 10
        })
        return params

    def execute(self, i = {}):
        sizes = (i.get('width'), i.get('height'))

        previews = []
        path = i.get('path')

        with VideoFileClip(path) as video:
            duration = video.duration
            frag_len = (duration / i.get('frames'))
            __hash = get_random_hash(8)

            for i in range(0, i.get('frames')):
                _state = ThumbnailState()
                _state.new(__hash)

                __new_prev = os.path.join(str(_state.get_dir()), f"{_state.hash}_{i}.jpg")

                _state.write_data({
                    "type": "photo",
                    "path": __new_prev,
                    "width": sizes[0],
                    "height": sizes[1]
                })

                previews.append(_state)

                i_duration = i * frag_len

                frame = video.get_frame(i_duration)
                img = Image.fromarray(frame)
                img.thumbnail(sizes, Image.LANCZOS)
                new_img = Image.new('RGB', sizes, (0, 0, 0))
                new_img.paste(
                    img,
                    ((sizes[0] - img.size[0]) // 2, (sizes[1] - img.size[1]) // 2)
                )

                new_img.save(__new_prev)
        
        return previews
