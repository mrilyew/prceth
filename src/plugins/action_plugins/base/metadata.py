from plugins.BasePlugins import BaseActionPlugin
from resources.globals import utils, createParser, extractMetadata

class metadata(BaseActionPlugin):
    name = 'base.metadata'
    allow_extensions = ['*']
    allow_type = 'entity'
    action = 'r'

    def run(self, input_entity=None, args=None):
        type = args.get('type')
        path = input_entity.getPath()
        parser = createParser(path)

        if not parser:
            print("No metadata")
            return ''
        
        metadata = extractMetadata(parser)
        if metadata:
            if type == 'arr':
                return metadata.exportPlaintext()
            else:
                return metadata
        else:
            raise ValueError("Error extracting metadata")
