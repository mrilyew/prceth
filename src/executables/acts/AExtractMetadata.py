from executables.acts.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils, createParser, extractMetadata

class AExtractMetadata(BaseAct):
    name = 'AExtractMetadata'
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
        
        parser = createParser(path)
        _metadata = None
        if not parser:
            return []
        
        with parser:
            try:
                _metadata = extractMetadata(parser)
                if _metadata == None:
                    raise ValueError

                return _metadata.exportPlaintext()
            except Exception as err:
                return []
