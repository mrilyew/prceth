from executables.representations import Representation
from submodules.Files.FileManager import file_manager
from pathlib import Path
from db.DbInsert import db_insert
from utils.MainUtils import proc_strtr, name_from_url
from declarable.ArgumentsTypes import StringArgument, LimitedArgument, CsvArgument
import os, mimetypes

class File(Representation):
    category = "Data"
    docs = {
        "definition": "data_file_definition",
        "name": "data_file_name_of",
    }
    executable_cfg = {
        "variants": [
            {
                "name": "representations.data.file.variant.path",
                "list": ["path", "type"],
            },
            {
                "name": "variant_by_url",
                "list": ["url"],
            }
        ]
    }

    @classmethod
    def declare(cls):
        params = {}
        params["path"] = CsvArgument({
            "orig": StringArgument({}),
            "docs": {
                "name": 'data_file_path',
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
                "name": "data_file_type",
                "values": {
                    "copy": {
                        "name": "data_file_type_copy",
                    },
                    "move": {
                        "name": "data_file_type_move"
                    },
                    "link": {
                        "name": "data_file_type_link"
                    },
                }
            },
            "values": ["copy", "move", "link"],
            "default": "copy",
        })
        params["url"] = CsvArgument({
            "docs": {
                "name": "data_file_url"
            },
            "orig": StringArgument({}),
            "default": None,
            "assertion": {
                "only_when": [
                    {"path": {"operator": "==", "value": None}}
                ]
            }
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        def extractWheel(self, i = {}):
            if 'path' in i:
                return 'extractByPath'
            elif 'text' in i:
                return 'extractByContent'
            elif 'url' in i:
                return 'extractByUrl'

        async def process_item(self, item):
            return item

        async def extractByPath(self, i = {}):
            pathes = i.get('path')
            output = []

            for _path in pathes:
                path = Path(_path)
                move_type = i.get("type")
                link = None

                assert path.exists(), 'path does not exists'
                assert path.is_dir() == False, 'path is dir'
                assert move_type in ['copy', 'move', 'link'], 'invalid type'

                su = db_insert.storageUnit()
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

                out = db_insert.contentFromJson({
                    "source": {
                        'type': 'path',
                        'content': str(path),
                    },
                    'content': {
                        "export_as": str(move_type),
                        "format": str(path.suffix[1:]),
                    },
                    'links': [su],
                    'link_main': 0
                }, self.outer)

                out = await self.process_item(out)

                output.append(out)

            return output

        async def extractByContent(self, i = {}):
            text = i.get('text')
            extension = i.get('extension')

            su = db_insert.storageUnit()

            original_name = "blank"
            full_name = '.'.join([original_name, extension])
            path = os.path.join(su.temp_dir, full_name)

            file_manager.createFile(path, text)

            su.set_main_file(path)

            out = db_insert.contentFromJson({
                "source": {
                    'type': 'api',
                    'content': 'blank'
                },
                "content": {
                    "format": str(extension),
                },
                "name": "blank.txt",
                "links": [su],
                "link_main": 0
            }, self.outer)

            out = await self.process_item(out)

            return [out]

        async def extractByUrl(self, i = {}):
            from utils.WebUtils import is_generated_ext
            from submodules.Web.DownloadManager import download_manager

            urls = i.get('url')
            outs = []

            for url in urls:
                name, ext = name_from_url(url)

                su = db_insert.storageUnit()
                mime_ext = None

                tmp_dir = su.temp_dir
                tmp_path = Path(os.path.join(tmp_dir, "download.tmp"))
                result_name = '.'.join([name, ext])
                result_path = Path(os.path.join(tmp_dir, result_name))

                # Making HTTP request

                url_request = await download_manager.addDownload(end = url,dir = tmp_path)

                header_content_type = url_request.headers.get('Content-Type', '').lower()

                if ext == '' or is_generated_ext(ext):
                    mime_ext = mimetypes.guess_extension(header_content_type)
                    if mime_ext:
                        ext = mime_ext[1:]
                    else:
                        ext = 'html'

                tmp_path.rename(os.path.join(tmp_dir, result_path))
                file_size = result_path.stat().st_size

                su.write_data({
                    "extension": ext,
                    "upload_name": result_name,
                    "filesize": file_size,
                })

                out = db_insert.contentFromJson({
                    "links": [su],
                    "link_main": 0,
                    "source": {
                        'type': 'url',
                        'content': url
                    },
                    "content": {},
                }, self.outer)

                out = await self.process_item(out)

                outs.append(out)

            return outs

    async def metadata(self, i = {}):
        return []
