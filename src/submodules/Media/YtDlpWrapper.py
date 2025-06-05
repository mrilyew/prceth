from app.App import logger, config
import yt_dlp

class YtDlpWrapper:
    def download_hook(self, d):
        if d['status'] == 'downloading':
           percent_str_clear = d['_percent_str'].replace('[0;94m', '')
           percent_str = percent_str_clear
           percent_str = ''.join(chr for chr in percent_str if chr.isprintable())
           percent = percent_str.split('%')[0].strip()

           logger.log(name="progress",message=f"Downloaded {percent}%",section="YtDlp")
        elif d['status'] == 'finished':
           logger.log(name="success",message=f"Successfully downloaded",section="YtDlp")
    
    def __init__(self, opts):
        # 'outtmpl': 'downloads/%(title)s.mp4',
        self.ydl_opts = {'quiet': True, 'progress_hooks': [self.download_hook], "ratelimit": float(config.get("web.max_speed")) * 1024}
        #self.ydl_opts["quiet"] = False
        self.ydl_opts.update(opts)

        self.ydl = yt_dlp.YoutubeDL(self.ydl_opts)
