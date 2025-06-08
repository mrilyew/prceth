from executables.services.Base.Base import BaseService
from repositories.ExtractorsRepository import ExtractorsRepository
from app.App import logger

class RSS(BaseService):
    category = 'Common'
    rss_extr = None
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, i = {}):
        self.rss_extr = ExtractorsRepository().getByName('Syndication.RSSFeed')

        rss_url = self.config.get("url")

        __rss_extractor = self.rss_extr()
        rss_items = []

        __rss_extractor.link(rss_items)
        await __rss_extractor.safeExecute({
            'url': rss_url
        })

        final_items = []

        logger.log(message=f"Got total {len(rss_items)} items",kind='message',section='RSS')

        for item in rss_items:
            last_item_date = int(self.config.get("date_offset", 0))
            item_created = int(item.declared_created_at)

            if item_created > last_item_date:
                logger.log(message=f"Changed offset {last_item_date}->{item_created}",kind='message',section='RSSOffset')

                item.save()

                final_items.append(item.api_structure())

                self.config['date_offset'] = int(item_created)
                self.service_object.updateData(self.config)

        logger.log(message=f"Totally {len(final_items)} new items",kind='success',section='RSS')

        if len(final_items) > 0:
            self.service_object.save()
