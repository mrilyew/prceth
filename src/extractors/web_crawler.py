from extractors.Base import BaseExtractor
from resources.globals import Crawler, file_manager
from resources.exceptions import NotPassedException

class web_crawler(BaseExtractor):
    name = 'web_crawler'
    category = 'net'
    params = {
        "url": {
            "desc_key": "-",
            "type": "string",
            "maxlength": 3
        }
    }

    def execute(self, args):
        site_url = args.get("url", None)
        if site_url == None:
            raise NotPassedException("URL was not passed")
        
        crawler = Crawler(save_dir=self.temp_dir,args=args)
        crawler.start_crawl(url=site_url)
        crawler.print_screenshot()
        html = crawler.print_html()
        
        page_title = crawler.driver.title
        original_name = "site.html"
        
        file_manager.createFile(dir=self.temp_dir,filename=original_name,content=html)
        output_metadata = {
            "title": page_title
        }
        final = {
            'format': "html",
            'original_name': original_name,
            'filesize': len(html),
            'source': "url:"+site_url,
            'json_info': output_metadata,
            'another_file': "screenshot.png"
        }

        del crawler
        return final
