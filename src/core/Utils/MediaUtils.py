from resources.Globals import shutil

class MediaUtils():
    def isFFMPEGInstalled(self):
        ffmpeg_exists = shutil.which("ffmpeg") is not None

        return ffmpeg_exists

media_utils = MediaUtils()
