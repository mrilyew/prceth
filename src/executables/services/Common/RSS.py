from executables.services.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from repositories.ExtractorsRepository import ExtractorsRepository
from declarable.ArgumentsTypes import StringArgument

class RSS(BaseDeclaredAtDependent):
    category = 'Common'

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
        self.regular_extractor = ExtractorsRepository().getByName('Syndication.RSSFeed')
        self.pass_params = {
            "url": self.config.get('url'),
            'create_collection': False,
        }

        await super().execute(i)
