from executables.acts.Base.Base import BaseAct
from resources.Globals import often_params
from db.File import File
from hachoir.core import config as HachoirConfig
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class ExtractMetadata(BaseAct):
    name = "ExtractMetadata"
    category = "metadata"

    docs = {
        "description": {
            "name": {
                "ru": "Получить основную метаинформацию",
                "en": "Extract main metadata"
            },
            "definition": {
                "ru": "Возвращает основные метаданные из основного файла",
                "en": "Returns base metadata from main file"
            },
            "exceptions": [
                {
                    "type": "AssertionException",
                    "message": "path or file_id not passed",
                    "explanation": {
                        "ru": "Нужно передать параметр \"path\" либо \"file_id\"",
                        "en": "Its need to set \"path\" or \"file_id\" param",
                    }
                }
            ]
        },
    }

    main_args = {
        "list": ["path", "file_id"],
        "type": "or",
    }

    def declare():
        params = {}
        params["path"] = often_params.get("path")
        params["file_id"] = {
            "type": "int",
            "default": None,
            "docs": {
                "definition": {
                    "ru": "ID файла",
                    "en": "File ID",
                }
            },
        }

        return params

    async def execute(self, args={}):
        HachoirConfig.quiet = True

        Input_path = self.passed_params.get("path")
        Input_file = self.passed_params.get("file_id")
        Final_path = None

        assert Input_path != None and Input_file != None, "path or file_id not passed"

        if Input_path == None:
            Final_path = args.get("path")
        else:
            file = File.get(Input_file)
            assert file != None, "invalid file"

            Final_path = file.getPath()

        assert Final_path != None, "input file not passed"

        __PARSER = createParser(Final_path)
        _metadata = None
        if not __PARSER:
            return []

        with __PARSER:
            try:
                _metadata = extractMetadata(__PARSER)
                if _metadata == None:
                    raise ValueError

                return _metadata.exportPlaintext()
            except Exception as err:
                return []
