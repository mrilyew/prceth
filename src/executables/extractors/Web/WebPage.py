from executables.extractors.Base import BaseExtractor
from resources.Globals import Crawler, file_manager, logger
from resources.Exceptions import NotPassedException
from db.File import File

class WebPage(BaseExtractor):
    name = 'WebPage'
    category = 'Web'
    manual_params = True

    # BTW, all requests will be unauthorized. So i recommend to use input raw html parser
    # TODO rewrite to multitab

    def declare():
        params = {}
        params["url"] = {
            "desc_key": "-",
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }

        return params
    
    async def run(self, args):
        TEMP_DIR = self.allocateTemp()

        SITE_URL = self.passed_params.get("url")
        self.crawler = Crawler(save_dir=TEMP_DIR,args=self.passed_params)
        if self.crawler.checkWebDriver() == False:
            await self.crawler.downloadChrome()

        self.crawler.startChrome()

        try:
            self.crawler.openURL(SITE_URL)
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

        ORIGINAL_NAME = "index.html"
        file_manager.createFile(dir=TEMP_DIR,filename=ORIGINAL_NAME,content=__html)
        output_metadata = self.crawler.printMeta()

        FILE = self._fileFromJson({
            "extension": "html",
            "upload_name": ORIGINAL_NAME,
            "filesize": len(__html),
        })
        ENTITY = self._entityFromJson({
            "source": "url:" + SITE_URL,
            "internal_content": output_metadata,
            "preview_file": "screenshot.png",
            "file": FILE
        })

        return {
            "entities": [
                ENTITY
            ],
        }
    
    async def postRun(self):
        await super().postRun()

        if getattr(self, "crawler", None):
            del self.crawler
    
    def onFail(self):
        super().onFail()
        
        if getattr(self, "crawler", None):
            del self.crawler

    def describeSource(self, INPUT_ENTITY):
        return {"type": "crawler", "data": {
            "source": INPUT_ENTITY.orig_source
        }}
