from executables.acts.Base.Base import BaseAct
from app.App import app, db_connection

class DisplayInfo(BaseAct):
    name = 'DisplayInfo'
    category = 'Meta'
    manual_params = True
    docs = {
        "description": {
            "name": {
                "ru": "Показ информации",
                "en": "Display information"
            },
            "definition": {
                "ru": "Показывает информацию из конфига и констант",
                "en": "Shows info from config and consts"
            }
        }
    }

    async def execute(self, args={}):
        return {
            "input": {
                "passed_args": self.passed_params,
                "argv": app.argv,
            }
        }
