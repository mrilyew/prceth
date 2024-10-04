from plugins.BasePlugins import BaseUploadPlugin
from pathlib import Path
from db.db import Entity
from core.utils import utils
import requests
import mimetypes
from urllib.parse import urlparse

class url(BaseUploadPlugin):
    name = 'base.url'
    format = 'url=%'
    works = 'all'
    category = 'base'

    def run(self, args=None):
        url = args.get('url')

        if url == None:
            raise AttributeError("URL was not passed")
        
        parsed_url = urlparse(url)
        file_name = url
        if url.find('/'):
            file_name = parsed_url.path.split('/')[-1].split('?')[0]

        file_name_splitted = file_name.split('.')
        file_name = file_name_splitted[0]
        ext = ''
        
        if len(file_name_splitted) > 1:
            ext = file_name_splitted[1]
        
        full_file_name = ''
        response = requests.get(url, allow_redirects=True)
        
        if response.status_code == 200:
            if file_name == '':
                file_name = requests.utils.quote(parsed_url.hostname) + '.'
            
            if ext == '':
                content_type = response.headers.get('Content-Type', '').lower()
                t_extension = mimetypes.guess_extension(content_type)
                if t_extension:
                    ext = t_extension[1:]
                else:
                    ext = 'html'
            
            full_file_name = ''.join([file_name, ext])
            save_path = Path(Entity.getTempPath() + '\\' + full_file_name)
            out_file = open(save_path, 'wb')
            out_file.write(response.content)
            out_file.close()
        else:
            raise FileNotFoundError('File not found')

        entity = Entity()
        entity.format = ext
        entity.original_name = full_file_name
        entity.display_name = full_file_name
        entity.filesize = save_path.stat().st_size
        entity.source = url

        return entity
