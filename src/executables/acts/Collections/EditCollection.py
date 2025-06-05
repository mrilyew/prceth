from resources.Globals import time, logger, asyncio, consts, config, Path, utils, file_manager, json
from executables.acts.Base.Base import BaseAct
from resources.Exceptions import NotPassedException, NotFoundException
from db.Collection import Collection
from db.ContentUnit import ContentUnit

class EditCollection(BaseAct):
    name = 'EditCollection'
    category = 'Collections'
    docs = {}

    def declare():
        params = {}

        return params

    async def execute(self, args={}):
        preview_ContentUnit = None
        if self.passed_params.get('collection_id', None) == None:
            raise NotPassedException("collection_id not passed")
        
        col = Collection.get(int(self.passed_params.get('collection_id')))
        if col == None:
            raise NotFoundException("Collection not found")
        
        if "preview_id" in self.passed_params:
            __preview_ContentUnit = ContentUnit.get(int(self.passed_params.get("preview_id")))
            if __preview_ContentUnit != None:
                preview_ContentUnit = __preview_ContentUnit
        
        if 'name' in self.passed_params and len(self.passed_params.get("name")) > 0:
            col.name = self.passed_params.get('name')
        if 'description' in self.passed_params:
            col.description = self.passed_params.get('description')
        if 'frontend_data' in self.passed_params:
            col.frontend_data = self.passed_params.get('frontend_data')
        if preview_ContentUnit != None:
            col.preview_id = preview_ContentUnit.id
        
        col.edited_at = time.time()
        col.save()
        
        return col
