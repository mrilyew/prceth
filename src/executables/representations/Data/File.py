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
                "name": "variant_by_path",
                "list": ["path", "type"],
            },
            {
                "name": "variant_by_text",
                "list": ["text", "extension"],
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
        params["path"] = StringArgument({
            "docs": {
                "name": 'data_file_path',
            },
            "default": None,
        })
        params["type"] = LimitedArgument({
            "docs": {
                "name": "data_file_type",
                "values": {
                    "copy": "data_file_type_copy",
                    "move": "data_file_type_move",
                    "link": "data_file_type_link",
                }
            },
            "values": ["copy", "move", "link"],
            "default": "copy",
            "assertion": {
                "only_when": [
                    {"path": {"operator": "!=", "value": None}}
                ]
            }
        })
        params["text"] = StringArgument({
            "docs": {
                "name": "data_file_text"
            },
            "default": None,
            "is_long": True,
        })
        params["extension"] = StringArgument({
            "docs": {
                "name": "data_file_extension"
            },
            "default": "txt",
            "maxlength": 6,
            "assertion": {
                "only_when": [
                    {"text": {"operator": "!=", "value": None}}
                ]
            }
        })
        params["url"] = CsvArgument({
            "docs": {
                "name": "data_file_url"
            },
            "default": None,
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

        async def extractByPath(self, i = {}):
            path = Path(i.get('path'))

            assert path.exists(), 'path does not exists'
            assert path.is_dir() == False, 'path is dir'

            su = db_insert.storageUnit()
            file_name = path.name
            move_type = i.get("type")
            move_to = Path(os.path.join(su.temp_dir, file_name))
            link = None

            assert move_type in ['copy', 'move', 'link'], 'invalid type'

            if move_type == 'copy':
                file_manager.copyFile(path, move_to)
            elif move_type == 'move':
                file_manager.moveFile(path, move_to)
            elif move_type == 'link':
                link = path
                #file_manager.symlinkFile(INPUT_PATH, MOVE_TO)

            if link == None:
                su.set_main_file(move_to)
            else:
                su.set_link(link)

            out = db_insert.contentFromJson({
                "source": {
                    'type': 'path',
                    'content': str(path),
                },
                'content': {
                    "export_as": str(move_type),
                },
                'links': [su],
                'link_main': 0
            })

            return [out]

        async def extractByContent(self, i = {}):
            text = i.get('text')
            original_name = "blank"
            extension = i.get('extension')
            full_name = '.'.join([original_name, extension])
            su = db_insert.storageUnit()
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
                    "text": proc_strtr(text, 100),
                },
                "name": "blank.txt",
                "links": [su],
                "link_main": 0
            })

            return [out]

        async def extractByUrl(self, i = {}):
            from utils.WebUtils import is_generated_ext
            from submodules.Web.DownloadManager import download_manager

            urls = i.get('url')
            out  = []

            for url in urls:
                name, ext = name_from_url(url)

                su = db_insert.storageUnit()
                tmp_dir = su.temp_dir
                tmp_save_path = Path(os.path.join(tmp_dir, "download.tmp"))
                mime_ext = None
                result_name = '.'.join([name, ext])
                result_path = Path(os.path.join(tmp_dir, result_name))

                # Making HTTP request

                url_request = await download_manager.addDownload(end = url,dir = tmp_save_path)
                content_type_header = url_request.headers.get('Content-Type', '').lower()

                if ext == '' or is_generated_ext(ext):
                    mime_ext = mimetypes.guess_extension(content_type_header)
                    if mime_ext:
                        ext = mime_ext[1:]
                    else:
                        ext = 'html'

                tmp_save_path.rename(os.path.join(tmp_dir, result_path))
                file_size = result_path.stat().st_size

                output_metadata = {
                    "mime": str(mime_ext),
                }

                su.write_data({
                    "extension": ext,
                    "upload_name": result_name,
                    "filesize": file_size,
                })
                out.append(db_insert.contentFromJson({
                    "links": [su],
                    "link_main": 0,
                    "source": {
                        'type': 'url',
                        'content': url
                    },
                    "content": output_metadata,
                }))

            return out

    async def metadata(self, i = {}):
        return []
