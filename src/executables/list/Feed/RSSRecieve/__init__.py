from executables.extractors import Extractor
from app.App import logger
from utils.MediaUtils import rss_date_parse
from executables.list.Data.Json import Implementation as JsonRepresentation
from declarable.Arguments import StringArgument, BooleanArgument
import aiohttp, xmltodict

class Implementation(Extractor):
    def declare():
        params = {}
        params["url"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["create_collection"] = BooleanArgument({
            "default": True,
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

        out = await JsonRepresentation.extract({
            'object': items
        })

        for i in out:
            i.extractor = self.full_name()

            __name = i.json_content.get("title", "Untitled")
            __date = rss_date_parse(i.json_content.get("pubDate"))

            i.display_name = str(__name)
            i.declared_created_at = __date.timestamp()

            self.linked_dict.append(i)
