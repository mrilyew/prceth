from executables.acts.Base import BaseAct
from hachoir.core import config
from resources.Globals import utils, createParser, extractMetadata

class AExtractMetadata(BaseAct):
    name = 'AExtractMetadata'
    category = 'metadata'
    accepts = 'entity'

    def execute(self, i, args=None):
        config.quiet = True

        EXPORT_TYPE = args.get('type', 'arr')
        PATH = None
        #if args.get("input_file", None) != None:
            #PATH = args.get("input_file")
        #else:
        assert i != None, "input entity not passed"
        
        PATH = i.getPath()
        
        __PARSER = createParser(PATH)
        _metadata = None
        if not __PARSER:
            return []
        
        with __PARSER:
            try:
                _metadata = extractMetadata(__PARSER)
                if _metadata == None:
                    raise ValueError

                return _metadata.exportPlaintext()
            except Exception as err:
                return []
