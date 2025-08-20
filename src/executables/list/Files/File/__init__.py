from executables.representations import Representation
from submodules.Files.FileManager import file_manager
from pathlib import Path
from utils.MainUtils import proc_strtr, name_from_url
from declarable.ArgumentsTypes import StringArgument, LimitedArgument, CsvArgument, StorageUnitArgument
import os, mimetypes

class Implementation(Representation):
    docs = {
        "definition": "representations.data.file.definition",
        "name": "representations.data.file.name",
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
        params["url"] = CsvArgument({
            "docs": {
                "name": "representations.data.file.url.name"
            },
            "orig": StringArgument({}),
            "default": None,
            "assertion": {
                "only_when": [
                    {"path": {"operator": "==", "value": None}}
                ]
            }
        })
        params["storage_unit"] = CsvArgument({
            "orig": StorageUnitArgument({}),
            "docs": {
                "name": "representations.data.file.storage_unit.name"
            },
            "default": None,
        })

        return params

    class Extractor(Representation.ExtractStrategy):
        def extractWheel(self, i = {}):
            if 'path' in i:
                return 'extractByPath'
            elif 'storage_unit' in i:
                return 'extractByStorageUnit'
            elif 'text' in i:
                return 'extractByContent'
            elif 'url' in i:
                return 'extractByUrl'

        async def process_item(self, item):
            return item

        async def extractByPath(self, i = {}):
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

        async def extractByContent(self, i = {}):
            text = i.get('text')
            extension = i.get('extension')

            out = self.ContentUnit()
            su = self.StorageUnit()

            original_name = "blank"
            full_name = '.'.join([original_name, extension])
            path = os.path.join(su.temp_dir, full_name)

            file_manager.createFile(path, text)
            su.set_main_file(path)

            out.source = {
                "type": "api",
                "content": original_name
            }
            out.content = {
                "format": str(extension),
            }
            out.display_name = full_name
            out.add_link(su)
            out.set_common_link(su)
            out = await self.process_item(out)

            return [out]

        async def extractByUrl(self, i = {}):
            from utils.WebUtils import is_generated_ext
            from submodules.Web.DownloadManager import download_manager

            urls = i.get('url')
            outs = []

            for url in urls:
                name, ext = name_from_url(url)

                out = self.ContentUnit()
                su = self.StorageUnit()

                tmp_dir = su.temp_dir
                tmp_path = Path(os.path.join(tmp_dir, "download.tmp"))
                result_name = '.'.join([name, ext])
                result_path = Path(os.path.join(tmp_dir, result_name))

                # Making HTTP request

                url_request = await download_manager.addDownload(end = url,dir = tmp_path)

                header_content_type = url_request.headers.get('Content-Type', '').lower()
                mime_ext = None
                if ext == '' or is_generated_ext(ext):
                    mime_ext = mimetypes.guess_extension(header_content_type)
                    if mime_ext:
                        ext = mime_ext[1:]
                    else:
                        ext = 'html'

                tmp_path.rename(os.path.join(tmp_dir, result_path))

                su.write_data({
                    "extension": ext,
                    "upload_name": result_name,
                    "filesize": result_path.stat().st_size,
                })

                out.add_link(su)
                out.set_common_link(su)
                out.source = {
                    'type': 'url',
                    'content': url
                }
                out.content = {}
                out = await self.process_item(out)

                outs.append(out)

            return outs

        async def extractByStorageUnit(self, i = {}):
            su = i.get('storage_unit')
            outs = []

            for item in su:
                out = self.ContentUnit()

                out.add_link(item)
                out.set_common_link(item)
                out = await self.process_item(out)

                outs.append(out)

            return outs

    async def metadata(self, i = {}):
        return []
