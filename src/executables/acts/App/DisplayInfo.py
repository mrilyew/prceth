from executables.acts import BaseAct
from app.App import app

class DisplayInfo(BaseAct):
    name = 'DisplayInfo'
    category = 'App'

    async def execute(self, args = {}):
        return {
            "input": {
                "validated_args": args,
                "argv": app.argv,
            }
        }
