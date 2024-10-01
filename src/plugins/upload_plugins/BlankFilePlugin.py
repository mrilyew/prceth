from plugins.BasePlugins import BaseUploadPlugin
from components.utils import utils
from components.db import Entity

class BlankFilePlugin(BaseUploadPlugin):
    name = 'BlankFile'
    format = 'format=%&text=%'
    works = 'all'
    category = 'base'

    def run(self, input_data=None):
        pars = utils.parse_json(input_data)
        format = pars.get('format')
        text = pars.get('text')
        
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
