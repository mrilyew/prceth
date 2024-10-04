from plugins.BasePlugins import BaseUploadPlugin
from core.utils import utils
from db.db import Entity

class blank(BaseUploadPlugin):
    name = 'base.blank'
    format = 'format=%;text=%'
    works = 'all'
    category = 'base'

    def run(self, args=None):
        format = args.get('format')
        if format == None:
            format = 'txt'
        
        text = args.get('text')
        
        # Creating entity

        entity = Entity()
        entity.format = str(format)
        entity.original_name = 'blank.' + str(format)
        entity.display_name = 'blank'
        entity.filesize = 0

        path = Entity.getTempPath() + '\\' + entity.original_name
        stream = open(path, 'w', encoding='utf-8')
        if text != None:
            stream.write(text)
        
        stream.close()
        
        return entity
