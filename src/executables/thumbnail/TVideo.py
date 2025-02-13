from executables.thumbnail.Base import BaseThumbnail
from resources.Globals import VideoFileClip, Image, math

class TVideo(BaseThumbnail):
    name = 'TVideo'
    accept = ["mp4", "mov"]

    def run(self, entity, params={}):
        size = (200, 200)
        returns = []
        path = entity.getPath()
        if params.hasPreview():
            path = params.another_file
        
        with VideoFileClip(path) as video:
            duration = video.duration
            frag_len = (duration / 10)
            for i in range(0, 10):
                returns.append("photo_{0}".format(i))
                i_duration = i * frag_len

                frame = video.get_frame(i_duration)
                img = Image.fromarray(frame)
                img.thumbnail(size, Image.LANCZOS)
                new_img = Image.new('RGB', size, (0, 0, 0))
                new_img.paste(
                    img,
                    ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
                )
                new_img.save(entity.getDirPath() + "/thumbnail_photo_{0}.{1}".format(i, "jpg"))
        
        return {
            "previews": returns
        }
