from extractors.Base import BaseExtractor
from resources.globals import Path, file_manager, utils
from resources.exceptions import InvalidPassedParam
from core.wheels import metadata_wheel, additional_metadata_wheel

class nt_path(BaseExtractor):
    name = 'nt_path'
    name_key = "extractor_key_name_nt_path"
    desc_key = "extractor_key_desc_nt_path"
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
        path = args.get('path')
        type = args.get('type', 'link')
        if path == None:
            raise AttributeError("Path was not passed")
        
        input_path = Path(path)
        if input_path.exists() == False:
            raise FileNotFoundError("File was not found")
        
        if input_path.is_dir() == True:
            raise ValueError("Path is directory")
        
        input_file_name  = input_path.name
        input_file_ext   = str(input_path.suffix[1:]) # remove dot
        collection_dir   = self.temp_dir
        move_result_path = Path(collection_dir + '\\' + input_file_name)

        # Creating entity
        
        file_action = None
        if type == 'copy':
            file_action = file_manager.copyFile(input_path, move_result_path)
        elif type == 'move':
            file_action = file_manager.moveFile(input_path, move_result_path)
        elif type == 'link':
            file_action = file_manager.symlinkFile(input_path, move_result_path)
        else:
            raise InvalidPassedParam("Incorrect \"type\".")
        
        metadata_resp = metadata_wheel(input_file=str(input_path))
        output_metadata = {
            "int_q_input": str(input_path), 
            "int_q_type": str(type),
            "metadata": utils.extract_metadata_to_dict(metadata_resp),
        }
        output_metadata["additional_metadata"] = additional_metadata_wheel(input_file=str(input_path))
        
        return {
            'format': input_file_ext,
            'original_name': input_file_name,
            'source': "path:"+str(input_path),
            'filesize': file_action.get('filesize'),
            'json_info': output_metadata
        }
