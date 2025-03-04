from executables.extractors.Base import BaseExtractor
from resources.Globals import Crawler, file_manager, ExecuteResponse, logger
from resources.Exceptions import NotPassedException

class ERawHTML(BaseExtractor):
    name = 'ERawHTML'
    category = 'net'
    params = {
        "url": {
            "desc_key": "-",
            "type": "string",
            "maxlength": 3
        }
    }

    def passParams(self, args):
        self.passed_params = args

        super().passParams(args)
        assert self.passed_params.get("html") != None, "html was not passed"
        #assert self.passed_params.get("url") != None, "url was not passed"

    async def run(self, args):
        self.crawler = Crawler(save_dir=self.temp_dir,args=self.passed_params)
        if self.crawler.checkWebDriver() == False:
            await self.crawler.downloadChrome()

        self.crawler.startChrome()

        try:
            self.crawler.crawlPageFromRawHTML(html=self.passed_params.get("html"),url_help=self.passed_params.get("url", ""))
        except Exception as ecx:
            logger.logException(ecx,section="Extractors|Crawling")
            raise ecx
        
        if True:
            self.crawler.scrollAvailableContent()
        
        self.crawler.printHTML()
        __html = await self.crawler.reworkHTML()
        if int(self.passed_params.get("literally", 0)) == 1:
            self.crawler.writeDocumentHTML(__html)
        
        self.crawler.printScreenshot()
        original_name = "index.html"
        
        file_manager.createFile(dir=self.temp_dir,filename=original_name,content=__html)
        output_metadata = self.crawler.printMeta()

        source = self.passed_params.get("url", "")
        if source == "":
            source = "api:html"
        else:
            source = "url:" + source

        final = ExecuteResponse({
            "format": "html",
            "original_name": original_name,
            "source": source,
            "filesize": len(__html),
            "json_info": output_metadata,
            "another_file": "screenshot.png"
        })
        
        return final
    
    async def postRun(self):
        await super().postRun()
        
        if getattr(self, "crawler", None):
            del self.crawler
    
    def onFail(self):
        super().onFail()
        
        if getattr(self, "crawler", None):
            del self.crawler

    def describeSource(self, INPUT_ENTITY):
        return {"type": "api", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
