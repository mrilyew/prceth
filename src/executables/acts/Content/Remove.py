from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.ContentUnit import ContentUnit

class RemoveContentUnit(BaseAct):
    name = 'RemoveContentUnit'
    category = 'Entities'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        if 'id' not in self.passed_params:
            raise NotPassedException("--ContentUnit_id not passed")

        ContentUnit_id = self.passed_params.get("ContentUnit_id")
        delete_file = int(self.passed_params.get("delete_file", "0")) == 1
        if delete_file == None:
            delete_file = False

        ContentUnit = ContentUnit.get(ContentUnit_id)
        if ContentUnit == None:
            raise NotFoundException("ContentUnit not found")
        
        ContentUnit.delete(delete_file=delete_file)

        return 1
