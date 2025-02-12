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

    def execute(self, args):
        input_path_text = args.get("path")
        export_type = args.get("type", "link") # As you will see: "copy", "move", "link"
        if input_path_text == None:
            raise NotPassedException("path was not passed")
        
        input_path = Path(input_path_text)
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
        if export_type == 'copy':
            file_action = file_manager.copyFile(input_path, move_result_path)
        # Copying and removing original file
        elif export_type == 'move':
            file_action = file_manager.moveFile(input_path, move_result_path)
        # Making a symlink to original file
        elif export_type == 'link':
            file_action = file_manager.symlinkFile(input_path, move_result_path)
        else:
            raise InvalidPassedParam("Invalid \"type\"")
        
        # Catching metadata
        file_metadata = metadata_wheel(input_file=str(input_path))
        output_metadata = {
            "original_path": str(input_path), 
            "export_type": str(export_type),
            "metadata": utils.extract_metadata_to_dict(file_metadata),
        }
        # TODO
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(input_path))
        
        return ExecuteResponse(
            format=str(input_file_ext),
            original_name=input_file_name,
            source="path:"+str(input_path),
            filesize=file_action.get('filesize'),
            json_info=output_metadata
        )
