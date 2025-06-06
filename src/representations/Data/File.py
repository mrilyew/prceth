from representations.Representation import Representation
from resources.Descriptions import descriptions
from db.StorageUnit import StorageUnit
from submodules.Files.FileManager import file_manager
from resources.Exceptions import InvalidPassedParam
from submodules.Web.DownloadManager import download_manager
from pathlib import Path
from utils.MainUtils import proc_strtr, name_from_url
from utils.WebUtils import is_generated_ext
import os, mimetypes

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
                    {"path": {"operator": "!=", "value": None}}
                ]
            }
        }
        params["text"] = {
            "type": "string",
            "default": None,
        }
        params["extension"] = {
            "docs": {
                "definition": descriptions.get('__file_extension')
            },
            "default": "txt",
            "type": "string",
            "maxlength": 6,
            "assertion": {
                "only_when": [
                    {"text": {"operator": "!=", "value": None}}
                ]
            }
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

        out = self.new_cu({
            "source": {
                'type': 'path',
                'content': str(i_path),
            },
            'content': __out_metadata,
            'main_su': su
        })

        return [out]

    async def extractByContent(self, i = {}):
        text = i.get('text')
        original_name = "blank"
        extension = i.get('extension')
        full_name = '.'.join([original_name, extension])

        su = StorageUnit()
    
        file_manager.createFile(filename=full_name,
            dir = su.temp_dir,
            content = text
        )

        su.write_data({
            "extension": i.get("extension"),
            "upload_name": full_name,
            "filesize": len(i.get("text").encode('utf-8')),
        })

        out = self.new_cu({
            "source": {
                'type': 'api',
                'content': 'blank'
            },
            "content": {
                "format": str(extension),
                "text": proc_strtr(text, 100),
            },
            "suggested_name": "blank.txt",
            "main_su": su
        })

        return [out]

    async def extractByUrl(self, i = {}):
        url = i.get('url')
        name, ext = name_from_url(url)

        su = StorageUnit()
        tmp_dir = su.temp_dir

        # Making HTTP request
        save_path = Path(os.path.join(tmp_dir, "download.tmp"))

        url_request = await download_manager.addDownload(end = url,dir = save_path)
        content_type_header = url_request.headers.get('Content-Type', '').lower()
        mime_ext = None

        if ext == '' or is_generated_ext(ext):
            mime_ext = mimetypes.guess_extension(content_type_header)
            if mime_ext:
                ext = mime_ext[1:]
            else:
                ext = 'html'
        
        result_name = '.'.join([name, ext])
        result_path = Path(os.path.join(tmp_dir, result_name))

        save_path.rename(os.path.join(tmp_dir, result_path))
        file_size = result_path.stat().st_size
        output_metadata = {
            "mime": str(mime_ext),
        }

        su.write_data({
            "extension": ext,
            "upload_name": result_name,
            "filesize": file_size,
        })
        out = self.new_cu({
            "main_su": su,
            "source": {
                'type': 'url',
                'content': url
            },
            "content": output_metadata,
        })

        return [out]

    async def metadata(self, i = {}):
        return []
