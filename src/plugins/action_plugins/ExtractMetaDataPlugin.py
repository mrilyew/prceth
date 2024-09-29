from plugins.BasePlugins import BaseActionPlugin
from components.utils import utils
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class ExtractMetaDataPlugin(BaseActionPlugin):
    name = 'ExtractMetaData'
    allow_extensions = ['*']
    allow_type = 'entity'
    action = 'r'

    def run(self, input_entity=None, input_data=None):
        pars = utils.parse_json(input_data)
        type = pars.get('type')
        path = input_entity.getPath()
        parser = createParser(path)

        if not parser:
            print("Parser was not created")
            return None
        
        metadata = extractMetadata(parser)
        if metadata:
            if type == 'arr':
                return metadata.exportPlaintext()
            else:
                return metadata
        else:
            raise ValueError("Error extracting metadata")
