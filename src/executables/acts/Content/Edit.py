from resources.Globals import time, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.ContentUnit import ContentUnit
from resources.Exceptions import NotPassedException, NotFoundException

class EditContentUnit(BaseAct):
    name = 'EditContentUnit'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        ContentUnit_id = int(self.passed_params.get("ContentUnit_id"))
        assert ContentUnit_id != None, "ContentUnit_id not passed"

        display_name = self.passed_params.get("display_name")
        description = self.passed_params.get("description")
        internal_content = self.passed_params.get("internal_content")
        frontend_data = self.passed_params.get("frontend_data")

        ContentUnit = ContentUnit.get(ContentUnit_id)
        if ContentUnit == None:
            raise NotFoundException("ContentUnit not found")

        if display_name != None:
            ContentUnit.display_name = display_name
        if description != None:
            ContentUnit.description = description
        if internal_content != None:
            ContentUnit.internal_content = json.dumps(internal_content, ensure_ascii=False)
        if frontend_data != None:
            ContentUnit.frontend_data = json.dumps(frontend_data, ensure_ascii=False)

        ContentUnit.edited_at = time.time()
        ContentUnit.save()

        return ContentUnit.getApiStructure()
