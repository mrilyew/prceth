from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from app.App import app, db_connection

class DisplayInfo(BaseAct):
    name = 'DisplayInfo'
    category = 'Meta'

    async def execute(self, args = {}):
        return {
            "input": {
                "validated_args": args,
                "argv": app.argv,
            }
        }
