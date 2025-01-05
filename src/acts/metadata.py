from acts.Base import BaseAct
from resources.globals import utils, createParser, extractMetadata

class metadata(BaseAct):
    name = 'metadata'
    name_key = "act_key_name_metadata"
    desc_key = "act_key_desc_metadata"
    allow_type = 'entity'
    type = 'entities'

    def execute(self, args=None):
        type = args.get('type', 'arr')
        input_entity_str = args.get('input_entity')
        if input_entity_str == None:
            raise ValueError("_error_no_passed_input_entity")

        input_entity = utils.parse_entity(input_entity_str)
        if input_entity == None:
            raise ValueError("_error_no_input_entity")
        
        path = input_entity.getPath()
        parser = createParser(path)
        if not parser:
            return ''
        
        metadata = extractMetadata(parser)
        if metadata:
            if type == 'arr':
                return metadata.exportPlaintext()
            else:
                return metadata
        else:
            raise ValueError("_error_extracting_metadata")
