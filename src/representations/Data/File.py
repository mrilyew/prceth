from representations.Representation import Representation
from resources.Descriptions import descriptions
from db.StorageUnit import StorageUnit
from submodules.Files.FileManager import file_manager
from resources.Exceptions import InvalidPassedParam
from pathlib import Path
from db.ContentUnit import ContentUnit
import os

class File(Representation):
    category = "Data"

    def declare():
        params = {}
        params["path"] = {
            "type": "string",
            "default": None,
        }
        params["type"] = {
            "docs": {
                "definition": descriptions.get('__movement_type'),
                "values": {
                    "copy": descriptions.get('__copies_to_storage_folder'),
                    "move": descriptions.get('__moves_to_storage_folder'),
                    "link": descriptions.get('__creates_virtual_link_to_folder'),
                }
            },
            "type": "array",
            "values": ["copy", "move", "link"],
            "default": "copy",
            "assertion": {
                "only_when": [
                    {"path": {"operator": "==", "value": "wall"}}
                ]
            }
        }
        params["text"] = {
            "type": "string",
            "default": None,
        }
        params["url"] = {
            "type": "string",
            "default": None,
        }

        return params

    def extractWheel(self, i = {}):
        if 'path' in i:
            return 'extractByPath'
        elif 'text' in i:
            return 'extractByContent'
        elif 'url' in i:
            return 'extractByUrl'

    async def extractByPath(self, i = {}):
        i_path = Path(i.get('path'))

        assert i_path.exists(), 'path does not exists'
        assert i_path.is_dir() == False, 'path is dir'

        su = StorageUnit()
        __file_stat = i_path.stat()
        file_size = __file_stat.st_size
        file_name = i_path.name
        file_ext = str(i_path.suffix[1:]) # remove dot
        __move_to = Path(os.path.join(su.temp_dir, file_name))

        link = None

        if i.get("type") == 'copy':
            file_manager.copyFile(i_path, __move_to)
        elif i.get("type") == 'move':
            file_manager.moveFile(i_path, __move_to)
        elif i.get("type") == 'link':
            link = str(i_path)
            #file_manager.symlinkFile(INPUT_PATH, MOVE_TO)
        else:
            raise InvalidPassedParam("Invalid \"type\"")

        su.write_data({
            "extension": file_ext,
            "upload_name": file_name,
            "filesize": file_size,
            "link": link,
        })

        __out_metadata = {
            "export_as": str(i.get("type")),
        }

        out = ContentUnit.fromJson(self.self_insert({
            "source": {
                'type': 'path',
                'content': str(i_path),
            },
            'content': __out_metadata,
            'main_su': su
        }))

        return [out]

    async def extractByContent(self, i = {}):
        text = i.get('text')
        original_name = i.get('original_name')
        extension = i.get('extension')

    async def extractByUrl(self, i = {}):
        url = i.get('url')

    async def metadata(self, i = {}):
        return []
