from executables.thumbnail.Base import BaseThumbnail
from resources.Globals import VideoFileClip, Image, math, consts, utils, os

class TVideo(BaseThumbnail):
    name = 'TVideo'
    accept = ["mp4", "mov"]

    def run(self, entity, params={}):
        size = (200, 200)
        __previews = {
            "photo": []
        }

        path = entity.getPath()
        if params.hasPreview():
            path = params.another_file
        
        with VideoFileClip(path) as video:
            duration = video.duration
            frag_len = (duration / 10)

            for i in range(0, 10):
                __hash = utils.getRandomHash(8)
                __new_prev = os.path.join(entity.getDirPath(), f"{__hash}_thumb_{i}.jpg")
                __previews["photo"].append({
                    "path": f"{__hash}_thumb_{i}.jpg",
                    "width": 200,
                    "height": 200
                })
                
                i_duration = i * frag_len

                frame = video.get_frame(i_duration)
                img = Image.fromarray(frame)
                img.thumbnail(size, Image.LANCZOS)
                new_img = Image.new('RGB', size, (0, 0, 0))
                new_img.paste(
                    img,
                    ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
                )
                new_img.save(__new_prev)
        
        return __previews
