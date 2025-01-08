from acts.Base import BaseAct
from hachoir.core import config
from resources.globals import utils, createParser, extractMetadata

class metadata(BaseAct):
    name = 'metadata'
    allow_type = 'entity'
    type = 'entities'

    def execute(self, args=None):
        config.quiet = True

        type = args.get('type', 'arr')
        input_entity_str = args.get('input_entity')
        path = None
        if args.get("input_file", None) != None:
            path = args.get("input_file")
        else:
            if input_entity_str == None:
                raise ValueError("_error_no_passed_input_entity")

            input_entity = utils.parse_entity(input_entity_str, ["entity"])
            if input_entity == None:
                raise ValueError("_error_no_input_entity")
            
            path = input_entity.getPath()
        
        try:
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
        except Exception:
            return []
