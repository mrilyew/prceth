from executables.extractors.Base import BaseExtractor
from resources.Globals import Path, file_manager, utils
from resources.Exceptions import InvalidPassedParam, NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel
from db.File import File

class FSPath(BaseExtractor):
    name = 'FSPath'
    category = 'Files'
    params = {
        "path": {
            "desc_key": "extractor_key_desc_path_path",
            "type": "string",
            "maxlength": 3
        },
        "type": {
            "desc_key": "extractor_key_desc_path_text",
            "type": "array",
            "values": ["copy", "move", "link"]
        }
    }

    def setArgs(self, args):
        self.passed_params["path"] = str(args.get("path"))
        self.passed_params["type"] = args.get("type", "copy")

        super().setArgs(args)
        assert args.get("path") != None, "path was not passed"
        assert self.passed_params.get("type") != None, "type was not passed"
    
    async def run(self, args):
        INPUT_PATH = Path(self.passed_params.get("path"))
        if INPUT_PATH.exists() == False:
            raise FileNotFoundError("Path does not exists")
        
        if INPUT_PATH.is_dir() == True:
            raise IsADirectoryError("Path is directory")
        
        FILE_STAT = INPUT_PATH.stat()
        FILE_SIZE = FILE_STAT.st_size
        INPUT_FILE_NAME  = INPUT_PATH.name
        INPUT_FILE_EXT   = str(INPUT_PATH.suffix[1:]) # remove dot
        MOVE_TO = Path(self.temp_dir + '\\' + INPUT_FILE_NAME)

        # Creating entity
        # Copying and leaving original file
        if self.passed_params.get("type") == 'copy':
            file_manager.copyFile(INPUT_PATH, MOVE_TO)
        # Copying and removing original file
        elif self.passed_params.get("type") == 'move':
            file_manager.moveFile(INPUT_PATH, MOVE_TO)
        # Making a symlink to original file
        elif self.passed_params.get("type") == 'link':
            file_manager.symlinkFile(INPUT_PATH, MOVE_TO)
        else:
            raise InvalidPassedParam("Invalid \"type\"")
        
        # Catching metadata
        __METADATA = metadata_wheel(input_file=str(INPUT_PATH))
        __OUTPUT_METADATA = {
            "export_as": str(self.passed_params.get("type")),
            "metadata": utils.extract_metadata_to_dict(__METADATA),
        }
        # TODO
        __OUTPUT_METADATA["additional_metadata"] = additional_metadata_wheel(input_file=str(INPUT_PATH))

        FILE = self._fileFromJson({
            "extension": INPUT_FILE_EXT,
            "upload_name": INPUT_FILE_NAME,
            "filesize": FILE_SIZE,
        })
        ENTITY = self._entityFromJson({
            "source": "path:"+str(INPUT_PATH),
            "entity_internal_content": __OUTPUT_METADATA,
            "indexation_content": {
                "metadata": __OUTPUT_METADATA["metadata"]
            },
            "file": FILE
        })
        
        return {
            "entities": [
                ENTITY
            ],
        }
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
