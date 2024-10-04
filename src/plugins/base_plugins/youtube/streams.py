from plugins.BasePlugins import BasePlugin
from core.utils import utils
from db.db import Entity
import json
import yt_dlp

class ExtractYoutubeVideoStreamsPlugin(BasePlugin):
    name = 'ExtractYoutubeStreams'

    def run(self, args=None):
        url = args.get('url')

        dlp = yt_dlp.YoutubeDL({
            'listformats': True,
            'quiet': True
        })
        info = dlp.extract_info(url, download=False)
        json_data = dlp.sanitize_info(info)
        formatted_formats = []

        for format in json_data.get('formats'):
            formatted_formats.append({
                'format': format.get('format'),
                'format_id': format.get('format_id'),
                'format_note': format.get('format_note'),
                'fps': format.get('fps'),
                'quality': format.get('quality'),
                'vcodec': format.get('vcodec'),
                'acodec': format.get('acodec'),
                'resolution': format.get('resolution'),
                'abr': format.get('abr'),
                'vbr': format.get('vbr'),
                'video_ext': format.get('video_ext'),
                'audio_ext': format.get('audio_ext'),
            })

        return formatted_formats
