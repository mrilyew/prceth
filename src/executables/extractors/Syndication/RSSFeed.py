from executables.extractors.Base.Base import BaseExtractor
from app.App import logger
from resources.Descriptions import descriptions
from utils.MediaUtils import rss_date_parse
from representations.Data.Json import Json as JsonRepresentation
from declarable.ArgumentsTypes import StringArgument, BooleanArgument
import aiohttp, xmltodict

class RSSFeed(BaseExtractor):
    category = 'Syndication'
    docs = {}

    def declare():
        params = {}
        params["url"] = StringArgument({
            "docs": {
                "definition": descriptions.get('__url_to_rss_feed')
            },
            "assertion": {
                "not_null": True,
            },
        })
        params["create_collection"] = BooleanArgument({
            "docs": {
                "definition": descriptions.get('__is_create_collection_enabled')
            },
            "default": True,
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def execute(self, i={}):
        __call_url = i.get("url")
        __response = None

        async with aiohttp.ClientSession() as session:
            async with session.get(__call_url) as response:
                __response = await response.text()

        logger.log(f"Called passed URL", section="RSS")

        __rss = xmltodict.parse(__response)

        __object_rss = __rss.get('rss')
        channel = __object_rss.get('channel')

        items = channel.get('item')
        if channel != None:
            try:
                del channel['item']
            except:
                pass

            if i.get('create_collection') == True:
                self.add_after.append(self.collectionable({
                    'name': channel.get('title', 'Untitled'),
                    'description': channel.get('description'),
                    'content': channel,
                    'declared_created_at': rss_date_parse(channel.get("pubDate")),
                    'source': {
                        'type': 'url',
                        'content': channel.get('link')
                    }
                }))

        out = await JsonRepresentation().extractByObject({
            'object': items
        })

        for i in out:
            i.extractor = self.full_name()

            __name = i.json_content.get("title", "Untitled")
            __date = rss_date_parse(i.json_content.get("pubDate"))

            i.display_name = str(__name)
            i.declared_created_at = __date.timestamp()

            self.linked_dict.append(i)
