from executables.acts import Act
from app.App import app

keys = {
    "name": {
        "ru_RU": "Отображение информации",
        "en_US": "App info display",
    },
}

class Implementation(Act):
    docs = {
        'name': keys.get("name")
    }

    async def execute(self, args = {}):
        return {
            "input": {
                "validated_args": args,
                "argv": app.argv,
            }
        }
