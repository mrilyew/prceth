from executables.acts.Base import BaseAct
from hachoir.core import config
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class ExtractMetadata(BaseAct):
    name = "ExtractMetadata"
    category = "metadata"
    accepts = "file"

    async def execute(self, i, args={}):
        config.quiet = True

        EXPORT_TYPE = args.get("INPUT_TYPE", "file")
        PATH = None
        assert i != None, "input file not passed"

        if EXPORT_TYPE == "file":
            PATH = i.getPath()
        else:
            PATH = i

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
