from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection

class DisplayInfo(BaseAct):
    name = 'DisplayInfo'
    category = 'Meta'
    docs = {
        "name": {
            "ru": "Показ информации",
            "en": "Display information"
        },
        "definition": {
            "ru": "Показывает информацию из конфига и констант",
            "en": "Shows info from config and consts"
        }
    }

    async def execute(self, args = {}):
        return {
            "input": {
                "validated_args": args,
                "argv": app.argv,
            }
        }
