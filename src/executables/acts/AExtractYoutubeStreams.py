from executables.acts.Base import BaseAct
from resources.Globals import yt_dlp, json, utils

class AExtractYoutubeStreams(BaseAct):
    name = 'AExtractYoutubeStreams'
    category = 'web'
    accepts = 'string'

    def execute(self, i, args=None):
        URL = i
        assert URL != None

        dlp = yt_dlp.YoutubeDL({
            'listformats': True,
            'quiet': True
        })
        __INFO = dlp.extract_info(URL, download=False)
        JSON_DATA = dlp.sanitize_info(__INFO)
        FMTS = []
        for __format in JSON_DATA.get('formats'):
            FMTS.append(__format)

        return FMTS
