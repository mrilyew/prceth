from executables.extractors.Base.Base import BaseExtractor
from resources.Globals import file_manager, utils
from db.File import File

class BlankFile(BaseExtractor):
    name = 'BlankFile'
    category = 'Files'
    #hidden = True
    docs = {
        "description": {
            "name": {
                "ru": "Пустой файл",
                "en": "Blank File"
            },
            "definition": {
                "ru": "Создаёт текстовый файл",
                "en": "Creates text file"
            }
        }
    }

    def declare():
        params = {}
        params["extension"] = {
            "docs": {
                "definition": {
                    "ru": "Расширение файла",
                    "en": "File extension",
                }
            },
            "default": "txt",
            "type": "string",
            "maxlength": 6,
        }
        params["text"] = {
            "docs": {
                "definition": {
                    "ru": "Текст файла",
                    "en": "File's content",
                }
            },
            "type": "string",
            "default": "",
        }
        params["__original_name"] = {
            "docs": {
                "definition": {
                    "ru": "Название файла",
                    "en": "File's name",
                }
            },
            "type": "string",
            "default": f"blank.txt",
            "hidden": True,
        }

        return params

    async def run(self, args):
        file_manager.createFile(filename=self.passed_params.get("__original_name"),
            dir=self.allocateTemp(),
            content=self.passed_params.get("text")
        )

        FILE = self._fileFromJson({
            "extension": self.passed_params.get("extension"),
            "upload_name": self.passed_params.get("__original_name"),
            "filesize": len(self.passed_params.get("text").encode('utf-8')),
        })
        ENTITY = self._entityFromJson({
            "source": "api:blank",
            "suggested_name": "blank.txt",
            "internal_content": {
                "format": str(self.passed_params.get("extension")),
                "text": utils.proc_strtr(self.passed_params.get("text"), 100),
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
