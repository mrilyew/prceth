from extractors.Base import BaseExtractor
from resources.globals import Path, file_manager

class nt_path(BaseExtractor):
    name = 'nt_path'
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
            "values": ["copy", "move"]
        }
    }

    def execute(self, args):
        path = args.get('path')
        type = args.get('type')
        if path == None:
            raise AttributeError("Path was not passed")
        
        input_path = Path(path)
        if input_path.exists() == False:
            raise FileNotFoundError("File was not found")
        
        if input_path.is_dir() == True:
            raise ValueError("Path is directory")
        
        input_file_name  = input_path.name
        input_file_ext   = input_path.suffix[1:] # remove dot
        collection_dir   = self.temp_dir
        move_result_path = Path(collection_dir + '\\' + input_file_name)

        # Creating entity
        
        file_action = None
        if type == 'copy':
            file_action = file_manager.copyFile(input_path, move_result_path)
        else:
            file_action = file_manager.moveFile(input_path, move_result_path)
        
        return {
            'format': str(input_file_ext),
            'original_name': input_file_name,
            'filesize': file_action.get('filesize')
        }
