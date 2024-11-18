from plugins.BasePlugins import BaseUploadPlugin
from resources.globals import files_utils

class blank(BaseUploadPlugin):
    name = 'base.blank'
    format = 'format=%;text=%'
    works = 'all'
    category = 'base'

    def run(self, args=None):
        format = args.get('format')
        text = args.get('text')
        if format == None:
            format = 'txt'
        
        original_name = 'blank.' + str(format)
        files_utils.createFile(filename=original_name,dir=self.temp_dir,content=text)
        if text == None:
            text = ''
        
        return {
            'format': str(format),
            'original_name': original_name,
            'filesize': len(text.encode('utf-8')),
        }
