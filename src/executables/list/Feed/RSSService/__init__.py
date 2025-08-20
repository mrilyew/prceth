from executables.services.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from executables.extractors import Extractor
from declarable.ArgumentsTypes import StringArgument

class Implementation(BaseDeclaredAtDependent):
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
        self.regular_extractor = Extractor.findByName('Syndication.RSSFeed')
        self.pass_params = {
            "url": self.config.get('url'),
            'create_collection': False,
        }

        await super().execute(i)
