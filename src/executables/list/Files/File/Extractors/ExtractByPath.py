from declarable.Arguments import StringArgument, LimitedArgument, CsvArgument
from executables.representations import Representation
from submodules.Files.FileManager import file_manager
from pathlib import Path
import os

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["path"] = CsvArgument({
            "orig": StringArgument({}),
            "docs": {
                "name": 'representations.data.file.path.name',
            },
            "default": None,
            "assertion": {
                "only_when": [
                    {"url": {"operator": "==", "value": None}}
                ]
            }
        })
        params["type"] = LimitedArgument({
            "docs": {
                "name": "representations.data.file.type.name",
                "values": {
                    "copy": {
                        "name": "representations.data.file.type.copy.name",
                    },
                    "move": {
                        "name": "representations.data.file.type.move.name"
                    },
                    "link": {
                        "name": "representations.data.file.type.link.name"
                    },
                }
            },
            "values": ["copy", "move", "link"],
            "default": "copy",
        })

        return params

    async def execute(self, i = {}):
        pathes = i.get('path')
        outs = []

        for _path in pathes:
            path = Path(_path)
            move_type = i.get("type")
            link = None

            assert path.exists(), 'path does not exists'
            assert path.is_dir() == False, 'path is dir'
            assert move_type in ['copy', 'move', 'link'], 'invalid type'

            out = self.ContentUnit()
            su = self.StorageUnit()

            file_name = path.name
            move_to = Path(os.path.join(su.temp_dir, file_name))

            match(move_type):
                case "copy":
                    file_manager.copyFile(path, move_to)
                    su.set_main_file(move_to)
                case "move":
                    file_manager.moveFile(path, move_to)
                    su.set_main_file(move_to)
                case "link":
                    su.set_link(link)
                    #file_manager.symlinkFile(INPUT_PATH, MOVE_TO)

            out.add_link(su)
            out.set_common_link(su)
            out.content = {
                "export_as": str(move_type),
                "format": str(path.suffix[1:]),
            }
            out.source = {
                "type": "path",
                "content": str(path)
            }
            out = await self.process_item(out)

            outs.append(out)

        return outs
