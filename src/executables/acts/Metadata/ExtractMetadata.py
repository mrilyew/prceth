from app.App import logger
from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from hachoir.core import config as HachoirConfig
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from utils.MainUtils import extract_metadata_to_dict
from declarable.ArgumentsTypes import StringArgument, BooleanArgument, StorageUnitArgument

class ExtractMetadata(BaseAct):
    category = 'Metadata'
    docs = {}
    executable_cfg = {
        "list": ["path", "su_id"],
        "type": "or",
    }

    @classmethod
    def declare(cls):
        params = {}
        params["path"] = StringArgument({
            "default": None,
            "docs": {
                "definition": descriptions.get("__path_to_file_where_get_metadata")
            },
        })
        params["su_id"] = StorageUnitArgument({
            "default": None,
            "docs": {
                "definition": descriptions.get("__su_id_where_get_metadata")
            },
        })
        params["convert_to_dict"] = BooleanArgument({
            "default": True,
            "docs": {
                "definition": descriptions.get("__is_convert_hachoir_metadata_to_dict")
            },
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
            assert input_file != None, "invalid storage_unit"

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

                if i.get('convert_to_dict'):
                    return extract_metadata_to_dict(_metadata.exportPlaintext())
                else:
                    return _metadata.exportPlaintext()
            except Exception as err:
                logger.logException(err,section="Acts?Metadata")

                return []
