from executables.extractors.Base import BaseExtractor
from resources.Globals import Path, file_manager, utils, ExecuteResponse
from resources.Exceptions import InvalidPassedParam, NotPassedException
from core.Wheels import metadata_wheel, additional_metadata_wheel

class EPath(BaseExtractor):
    name = 'EPath'
    category = 'base'
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

    def passParams(self, args):
        self.passed_params["path"] = str(args.get("path"))
        self.passed_params["type"] = args.get("type", "copy")

        super().passParams(args)
        assert args.get("path") != None, "path was not passed"
        assert self.passed_params.get("type") != None, "type was not passed"
    
    async def run(self, args):
        input_path = Path(self.passed_params.get("path"))
        if input_path.exists() == False:
            raise FileNotFoundError("Path does not exists")
        
        if input_path.is_dir() == True:
            raise IsADirectoryError("Path is directory")
        
        input_file_name  = input_path.name
        input_file_ext   = str(input_path.suffix[1:]) # remove dot
        collection_dir   = self.temp_dir
        move_result_path = Path(collection_dir + '\\' + input_file_name)

        # Creating entity
        
        file_action = None
        # Copying and leaving original file
        if self.passed_params.get("type") == 'copy':
            file_action = file_manager.copyFile(input_path, move_result_path)
        # Copying and removing original file
        elif self.passed_params.get("type") == 'move':
            file_action = file_manager.moveFile(input_path, move_result_path)
        # Making a symlink to original file
        elif self.passed_params.get("type") == 'link':
            file_action = file_manager.symlinkFile(input_path, move_result_path)
        else:
            raise InvalidPassedParam("Invalid \"type\"")
        
        # Catching metadata
        file_metadata = metadata_wheel(input_file=str(input_path))
        output_metadata = {
            "original_path": str(input_path), 
            "export_type": str(self.passed_params.get("type")),
            "metadata": utils.extract_metadata_to_dict(file_metadata),
        }
        # TODO
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(input_path))
        
        return ExecuteResponse({
            "format": str(input_file_ext),
            "original_name": input_file_name,
            "source": "path:"+str(input_path),
            "filesize": file_action.get('filesize'),
            "entity_internal_content": output_metadata,
            "indexation_content": {
                "original_path": str(input_path), 
                "metadata": output_metadata["metadata"]
            }
        })
    
    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
