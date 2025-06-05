from resources.Globals import aiohttp, logger, xmltodict, datetime
from executables.extractors.Base.Base import BaseExtractor
from executables.extractors.Syndication.RSSItem import RSSItem

class RSSFeed(BaseExtractor):
    name = 'RSSFeed'
    category = 'Syndication'
    docs = {}

    def declare():
        params = {}
        params["url"] = {
            "docs": {
                "definition": {
                    "ru": "URL на RSS-фид",
                    "en": "URL to RSS-feed",
                }
            },
            "type": "string",
            "assertion": {
                "not_null": True,
            },
        }
        params["save_original_xml"] = {
            "docs": {
                "definition": {
                    "ru": "Сохранять оригинальный XML",
                    "en": "Save original XML",
                }
            },
            "default": False,
            "type": "bool",
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def run(self, args={}):
        __call_url = self.passed_params.get("url")
        __response = None

        async with aiohttp.ClientSession() as session:
            async with session.get(__call_url) as response:
                __response = await response.text()

        logger.log(f"Called {__call_url}", section="RSS")

        __rss = xmltodict.parse(__response)
        __object_rss = __rss.get("rss")
        __channel = __object_rss.get("channel")
        __items = __channel.get("item")

        __rss_item = self.fork(RSSItem, {
            "xml_parsed": __items, 
            "save_original_xml": self.passed_params.get("save_original_xml"),
            "source": __call_url,
        })

        return await __rss_item.execute({})
