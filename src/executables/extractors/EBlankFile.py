from executables.extractors.Base import BaseExtractor
from resources.Globals import file_manager, utils, ExecuteResponse

# hope its funny enough
class EBlankFile(BaseExtractor):
    name = 'EBlankFile'
    category = 'base'
    hidden = True
    params = {
        "format": {
            "desc_key": "extractor_key_desc_blank_format",
            "type": "string",
            "maxlength": 6
        },
        "text": {
            "desc_key": "extractor_key_desc_blank_text",
            "type": "string",
            "maxlength": -1
        }
    }

    def execute(self, args):
        format = args.get("format", "txt")
        text = args.get("text", "")
        
        original_name = f"blank.{str(format)}"
        file_manager.createFile(filename=original_name,dir=self.temp_dir,content=text)

        return ExecuteResponse(
            format=str(format),
            original_name=original_name,
            source="api:blank",
            filesize=len(text.encode('utf-8')),
            json_info={
                "format": str(format),
                "text": utils.proc_strtr(text, 100),
            }
        )
