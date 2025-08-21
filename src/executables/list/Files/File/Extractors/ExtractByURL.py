from declarable.ArgumentsTypes import CsvArgument, StringArgument
from submodules.Web.DownloadManager import download_manager
from executables.representations import Representation
from utils.WebUtils import is_generated_ext
from utils.MainUtils import name_from_url
from pathlib import Path
import mimetypes, os

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
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

        return params
    
    async def execute(self, i = {}):
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
