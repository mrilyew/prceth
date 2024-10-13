from plugins.BasePlugins import BaseUploadPlugin
from resources.globals import yt_dlp, json, Entity, utils

class video(BaseUploadPlugin):
    name = 'youtube.video'
    format = 'url=%'
    works = 'all'
    category = 'youtube'

    def run(self, args=None):
        url = args.get('url')
        format_id = args.get('format_id')

        if url == None:
            print('No "url" or "format_id"')
            exit()

        if format_id == None:
            format_id = 'bestvideo+bestaudio/best'
        
        cached_content = {}
        opts = {
            'format': format_id,
            'noplaylist': True,
            'outtmpl': f"{Entity.getTempPath()}\\%(id)s.%(ext)s",
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegMerger',
            }],
        }

        dlp = yt_dlp.YoutubeDL(opts)
        info_dict_uns = dlp.extract_info(url, download=True)
        info_dict = dlp.sanitize_info(info_dict_uns)
        info_dict.pop('formats')
        info_dict.pop('requested_downloads')
        info_dict.pop('http_headers')
        info_dict.pop('_format_sort_fields')
        info_dict.pop('_version')
        info_dict.pop('_has_drm')
        info_dict.pop('_type')

        if args.get('save_automatic_captions') == None:
            info_dict.pop('automatic_captions')

        orig_name = info_dict.get('id') + '.' + info_dict['ext']

        cached_content = info_dict
        
        entity = Entity()
        entity.format = info_dict.get('ext')
        entity.original_name = orig_name
        entity.display_name = info_dict.get('fulltitle')
        entity.source = info_dict.get('webpage_url')
        entity.cached_info = json.dumps(cached_content, separators=(',', ':'))

        return entity
