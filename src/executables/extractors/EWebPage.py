from executables.extractors.Base import BaseExtractor
from resources.Globals import Crawler, file_manager, ExecuteResponse, logger
from resources.Exceptions import NotPassedException

class EWebPage(BaseExtractor):
    name = 'EWebPage'
    category = 'net'
    params = {
        "url": {
            "desc_key": "-",
            "type": "string",
            "maxlength": 3
        }
    }

    # BTW, all requests will be unauthorized. So we need to use input raw html parser
    # TODO rewrite to multitab
    async def execute(self, args):
        site_url = args.get("url", None)
        if site_url == None or site_url == "":
            raise NotPassedException("url was not passed")
        
        self.crawler = Crawler(save_dir=self.temp_dir,args=args)
        if self.crawler.checkWebDriver() == False:
            self.crawler.downloadChrome()

        self.crawler.startChrome()

        try:
            self.crawler.openURL(site_url)
        except Exception as ecx:
            logger.logException(ecx,section="Extractors|Crawling")
            raise ecx
         
        if True:
            self.crawler.scrollAvailableContent()
        
        self.crawler.printHTML()
        __html = await self.crawler.reworkHTML()
        if False:
            self.crawler.writeDocumentHTML(__html)

        self.crawler.printScreenshot()

        original_name = "index.html"
        file_manager.createFile(dir=self.temp_dir,filename=original_name,content=__html)
        output_metadata = self.crawler.printMeta()

        final = ExecuteResponse(
            format="html",
            original_name=original_name,
            source="url:"+site_url,
            filesize=len(__html),
            json_info=output_metadata,
            another_file="screenshot.png"
        )
        
        return final
    
    def cleanup(self, entity):
        super().cleanup(entity=entity)
        
        del self.crawler
    
    def cleanup_fail(self):
        super().cleanup_fail()
        
        del self.crawler
