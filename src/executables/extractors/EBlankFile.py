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

    def passParams(self, args):
        self.passed_params["format"] = args.get("format", "txt")
        self.passed_params["text"] = args.get("text", "")

        super().passParams(args)

    async def run(self, args):
        original_name = f"blank.{self.passed_params.get("format")}"
        file_manager.createFile(filename=original_name,dir=self.temp_dir,content=self.passed_params.get("text"))

        return ExecuteResponse({
            "format": str(self.passed_params.get("format")),
            "original_name": original_name,
            "source": "api:blank",
            "filesize": len(self.passed_params.get("text").encode('utf-8')),
            "json_info": {
                "format": str(self.passed_params.get("format")),
                "text": utils.proc_strtr(self.passed_params.get("text"), 100),
            }
        })

    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
