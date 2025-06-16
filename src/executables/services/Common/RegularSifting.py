from executables.services.Base.BaseDeclaredAtDependent import BaseDeclaredAtDependent
from repositories.ExtractorsRepository import ExtractorsRepository
from declarable.ArgumentsTypes import StringArgument, ObjectArgument

class RegularSifting(BaseDeclaredAtDependent):
    category = 'Common'

    @classmethod
    def declare(cls):
        params = {}
        params["extractor"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["pass_args"] = ObjectArgument({
            "default": {},
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def execute(self, i = {}):
        self.regular_extractor = ExtractorsRepository().getByName(self.config.get('extractor'))
        self.pass_params = self.config.get('pass_args')

        await super().execute(i)
