from executables.extractors.Base.Base import BaseExtractor
from app.App import logger
from resources.Descriptions import descriptions
from representations.Data.Json import Json as JsonRepresentation
from utils.MediaUtils import rss_date_parse
import aiohttp, xmltodict

class RSSFeed(BaseExtractor):
    name = 'RSSFeed'
    category = 'Syndication'
    docs = {}

    def declare():
        params = {}
        params["url"] = {
            "docs": {
                "definition": descriptions.get('__url_to_rss_feed')
            },
            "type": "string",
            "assertion": {
                "not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        __call_url = args.get("url")
        __response = None

        async with aiohttp.ClientSession() as session:
            async with session.get(__call_url) as response:
                __response = await response.text()

        logger.log(f"Called {__call_url}", section="RSS")

        __rss = xmltodict.parse(__response)

        __object_rss = __rss.get("rss")
        channel = __object_rss.get("channel")
        items = channel.get("item")

        out = await JsonRepresentation().extractByObject({
            'object': items
        })

        for i in out:
            i.extractor = self.full_name

            __name = i.json_content.get("title")
            __date = rss_date_parse(i.json_content.get("pubDate"))

            i.display_name = __name
            i.declared_created_at = __date.timestamp()

            self.linked_dict.append(i)
