from extractors.Base import BaseExtractor
from resources.globals import Crawler, file_manager
from resources.exceptions import NotPassedException

class raw_html(BaseExtractor):
    name = 'raw_html'
    category = 'net'
    params = {
        "url": {
            "desc_key": "-",
            "type": "string",
            "maxlength": 3
        }
    }

    def execute(self, args):
        html_text = args.get("html", None)
        possible_url = args.get("url", "")
        if html_text == None:
            raise NotPassedException("HTML was not passed")
        
        crawler = Crawler(save_dir=self.temp_dir,args=args)
        crawler.start_crawl_from_html(html=html_text,url_help=possible_url)
        crawler.print_screenshot()
        html = crawler.print_html()
        
        original_name = "index.html"
        
        file_manager.createFile(dir=self.temp_dir,filename=original_name,content=html)
        output_metadata = crawler.print_meta()

        source = possible_url
        if source == "":
            source = "api:html"
        else:
            source = "url:" + source
        
        final = {
            'format': "html",
            'original_name': original_name,
            'filesize': len(html),
            'source': source,
            'json_info': output_metadata,
            'another_file': "screenshot.png"
        }

        del crawler
        return final
