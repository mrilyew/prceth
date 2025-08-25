from executables.representations import Representation
from hachoir.core import config as HachoirConfig
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from utils.MainUtils import extract_metadata_to_dict
from declarable.Arguments import StringArgument, BooleanArgument, StorageUnitArgument
from app.App import logger

class Method(Representation.AbstractAct):
    required_modules = ["hachoir"]

    @classmethod
    def declare(cls):
        params = {}
        params["path"] = StringArgument({
            "default": None,
        })
        params["su_id"] = StorageUnitArgument({
            "default": None,
        })
        params["convert_to_dict"] = BooleanArgument({
            "default": True,
        })

        return params

    async def execute(self, i = {}):
        HachoirConfig.quiet = True

        input_path = i.get("path")
        input_file = i.get("su_id")
        final_path = None

        if input_path != None:
            final_path = input_path
        else:
            assert input_file != None, "invalid su_id"

            final_path = input_file.path()

        assert final_path != None, "input file not passed"

        __PARSER = createParser(final_path)
        _metadata = None
        if not __PARSER:
            return []

        with __PARSER:
            try:
                _metadata = extractMetadata(__PARSER)
                if _metadata == None:
                    raise ValueError

                if i.get('convert_to_dict') == True:
                    return extract_metadata_to_dict(_metadata.exportPlaintext())
                else:
                    return _metadata.exportPlaintext()
            except Exception as err:
                logger.logException(err,section="Acts!Metadata")

                return []
