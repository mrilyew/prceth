from declarable.Arguments import StringArgument
from executables.representations import Representation
from executables.list.Data.Json import Implementation as JsonRepresentation
from utils.MediaUtils import rss_date_parse
from app.App import logger
import aiohttp, xmltodict

class Method(Representation.AbstractExtractor):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def execute(self, i = {}):
        url = i.get("url")
        response_xml = None

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        logger.log(f"Called passed URL", section="RSS")

        rss_response = xmltodict.parse(response_xml)
        rss_object = rss_response.get('rss')
        rss_channel = rss_object.get('channel')

        items = rss_channel.get('item')
        if rss_channel != None:
            try:
                del rss_channel['item']
            except:
                pass

        if False:
            collection = self.ContentUnit()
            collection.display_name = channel.get('title', 'Untitled')
            collection.description = channel.get('description')
            collection.content = channel
            collection.declared_created_at = rss_date_parse(channel.get("pubDate"))
            collection.source = {
                'type': 'url',
                'content': channel.get('link')
            }
            collection.is_collection = True
            self.add_after.append(collection)

        out_items = []

        for i in items:
            out = self.ContentUnit()
            out.display_name = i.get("title", "Untitled")
            out.declared_created_at =  rss_date_parse(i.get("pubDate")).timestamp()

            out_items.append(i)

        return out_items
