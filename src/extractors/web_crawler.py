from extractors.Base import BaseExtractor
from resources.globals import Crawler
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
        
        crawler = Crawler(save_dir=self.temp_dir)
        crawler.crawl_site(site_url)
