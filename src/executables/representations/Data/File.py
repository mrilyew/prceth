from executables.representations.Representation import Representation
from submodules.Files.FileManager import file_manager
from pathlib import Path
from db.DbInsert import db_insert
from utils.MainUtils import proc_strtr, name_from_url
from declarable.ArgumentsTypes import StringArgument, LimitedArgument
from executables.representations.ExtractStrategy import ExtractStrategy
import os, mimetypes

class File(Representation):
    category = "Data"

    @classmethod
    def declare(cls):
        params = {}
        params["path"] = StringArgument({
            "default": None,
        })
        params["type"] = LimitedArgument({
            "docs": {
                "definition": '__movement_type',
                "values": {
                    "copy": '__copies_to_storage_folder',
                    "move": '__moves_to_storage_folder',
                    "link": '__creates_virtual_link_to_folder',
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
            "default": None,
        })
        params["extension"] = StringArgument({
            "docs": {
                "definition": '__file_extension'
            },
            "default": "txt",
            "maxlength": 6,
            "assertion": {
                "only_when": [
                    {"text": {"operator": "!=", "value": None}}
                ]
            }
        })
        params["url"] = StringArgument({
            "default": None,
        })

        return params

    class Extractor(ExtractStrategy):
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

            link = None
            file_stat = path.stat()
            file_size = file_stat.st_size
            file_name = path.name
            file_ext = str(path.suffix[1:]) # remove dot
            move_to = Path(os.path.join(su.temp_dir, file_name))

            assert i.get('type') in ['copy', 'move', link], 'invalid type'

            if i.get("type") == 'copy':
                file_manager.copyFile(path, move_to)
            elif i.get("type") == 'move':
                file_manager.moveFile(path, move_to)
            elif i.get("type") == 'link':
                link = str(path)
                #file_manager.symlinkFile(INPUT_PATH, MOVE_TO)

            su.write_data({
                "extension": file_ext,
                "upload_name": file_name,
                "filesize": file_size,
                "link": link,
            })

            out = db_insert.contentFromJson({
                "source": {
                    'type': 'path',
                    'content': str(path),
                },
                'content': {
                    "export_as": str(i.get("type")),
                },
                'links': [su]
            })

            return [out]

        async def extractByContent(self, i = {}):
            text = i.get('text')
            original_name = "blank"
            extension = i.get('extension')
            full_name = '.'.join([original_name, extension])

            su = db_insert.storageUnit()

            file_manager.createFile(filename=full_name,
                dir = su.temp_dir,
                content = text
            )

            su.write_data({
                "extension": i.get("extension"),
                "upload_name": full_name,
                "filesize": len(i.get("text").encode('utf-8')),
            })

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
                "links": [su]
            })

            return [out]

        async def extractByUrl(self, i = {}):
            from utils.WebUtils import is_generated_ext
            from submodules.Web.DownloadManager import download_manager

            url = i.get('url')
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
            out = db_insert.contentFromJson({
                "links": [su],
                "source": {
                    'type': 'url',
                    'content': url
                },
                "content": output_metadata,
            })

            return [out]

    async def metadata(self, i = {}):
        return []
