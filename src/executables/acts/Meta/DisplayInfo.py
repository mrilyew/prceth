from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from app.App import app, db_connection

class DisplayInfo(BaseAct):
    name = 'DisplayInfo'
    category = 'Meta'
    docs = {
        "name": descriptions.get('__info_showing'),
        "definition": descriptions.get('__shows_info_from_config_and_consts'),
    }

    async def execute(self, args = {}):
        return {
            "input": {
                "validated_args": args,
                "argv": app.argv,
            }
        }
