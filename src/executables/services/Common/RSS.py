from executables.services.Base.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from repositories.ExtractorsRepository import ExtractorsRepository
from resources.Descriptions import descriptions

class RSS(BaseDeclaredAtDependent):
    category = 'Common'
    rss_extr = None
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

    async def execute(self, i = {}):
        self.regular_extractor = ExtractorsRepository().getByName('Syndication.RSSFeed')
        self.pass_params = {
            "url": self.config.get('url'),
            'create_collection': False,
        }

        await super().execute(i)
