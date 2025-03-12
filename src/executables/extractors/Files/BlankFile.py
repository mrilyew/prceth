from executables.extractors.Base import BaseExtractor
from resources.Globals import file_manager, utils, ExecuteResponse
from db.File import File

class BlankFile(BaseExtractor):
    name = 'BlankFile'
    category = 'base'
    hidden = True
    params = {
        "extension": {
            "desc_key": "extractor_key_desc_blank_extension",
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
        self.passed_params["extension"] = args.get("extension", "txt")
        self.passed_params["text"] = args.get("text", "")

        super().passParams(args)

    async def run(self, args):
        original_name = f"blank.{self.passed_params.get("extension")}"
        file_manager.createFile(filename=original_name,
                                dir=self.temp_dir,
                                content=self.passed_params.get("text"))

        __file = File()
        __file.extension = self.passed_params.get("extension")
        __file.hash = utils.getRandomHash(32)
        __file.upload_name = original_name
        __file.filesize = len(self.passed_params.get("text").encode('utf-8'))
        __file.temp_dir = self.temp_dir
        
        __file.save()

        return ExecuteResponse({
            "source": "api:blank",
            "main_file": __file,
            "indexation_content": {
                "format": str(self.passed_params.get("extension")),
                "text": utils.proc_strtr(self.passed_params.get("text"), 100),
            },
        })

    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
