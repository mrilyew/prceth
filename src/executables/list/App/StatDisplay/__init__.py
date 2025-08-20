from executables.acts import Act
from app.App import app
from db.Models.Content.ContentUnit import ContentUnit

class Implementation(Act):
    async def execute(self, args = {}):
        content_units = ContentUnit.select().where(ContentUnit.deleted == 0)

        return {
            "content_units": {
                "total_count": content_units.count()
            }
        }
