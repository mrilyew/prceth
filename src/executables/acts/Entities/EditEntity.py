from resources.Globals import time, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from db.Entity import Entity
from resources.Exceptions import NotPassedException, NotFoundException

class EditEntity(BaseAct):
    name = 'EditEntity'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        entity_id = int(self.passed_params.get("entity_id"))
        assert entity_id != None, "entity_id not passed"

        display_name = self.passed_params.get("display_name")
        description = self.passed_params.get("description")
        internal_content = self.passed_params.get("internal_content")
        frontend_data = self.passed_params.get("frontend_data")

        entity = Entity.get(entity_id)
        if entity == None:
            raise NotFoundException("Entity not found")

        if display_name != None:
            entity.display_name = display_name
        if description != None:
            entity.description = description
        if internal_content != None:
            entity.internal_content = json.dumps(internal_content, ensure_ascii=False)
        if frontend_data != None:
            entity.frontend_data = json.dumps(frontend_data, ensure_ascii=False)

        entity.edited_at = time.time()
        entity.save()

        return entity.getApiStructure()
