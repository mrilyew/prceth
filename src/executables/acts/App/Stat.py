from executables.acts import BaseAct
from app.App import app
from db.Models.Content.ContentUnit import ContentUnit

class Stat(BaseAct):
    name = 'Stat'
    category = 'App'

    async def execute(self, args = {}):
        content_units = ContentUnit.select().where(ContentUnit.deleted == 0)

        return {
            "content_units": {
                "total_count": content_units.count()
            }
        }
