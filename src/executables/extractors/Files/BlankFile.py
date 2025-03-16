from executables.extractors.Base import BaseExtractor
from resources.Globals import file_manager, utils
from db.File import File

class BlankFile(BaseExtractor):
    name = 'BlankFile'
    category = 'Files'
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
        self.passed_params["__original_name"] = f"blank.{self.passed_params.get("extension")}"

        super().passParams(args)

    async def make(self):
        file_manager.createFile(filename=self.passed_params.get("__original_name"),
                                dir=self.temp_dir,
                                content=self.passed_params.get("text"))

    async def run(self, args):
        await self.make()

        return {
            "entities": [
                {
                    "source": "api:blank",
                    "suggested_name": "blank.txt",
                    "indexation_content": {
                        "format": str(self.passed_params.get("extension")),
                        "text": utils.proc_strtr(self.passed_params.get("text"), 100),
                    },
                    "file": {
                        "extension": self.passed_params.get("extension"),
                        # "hash": utils.getRandomHash(32),
                        "upload_name": self.passed_params.get("__original_name"),
                        "filesize": len(self.passed_params.get("text").encode('utf-8')),
                    }
                }
            ],
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
