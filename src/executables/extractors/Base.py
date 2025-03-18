from resources.Globals import storage, os, utils, file_manager, json, logger
from db.Entity import Entity

class BaseExtractor:
    name = 'base'
    category = 'template'
    passed_params = {}

    def __init__(self, temp_dir=None, del_dir_on_fail=True):
        self.passed_params = {}
        if temp_dir != None:
            self.temp_dir = temp_dir
        else:
            self.temp_dir = storage.makeTemporaryCollectionDir()
        
        self.del_dir_on_fail = del_dir_on_fail

    def setArgs(self, args):
        self.passed_params["display_name"] = args.get("display_name", None)
        self.passed_params["description"] = args.get("description", None)
        self.passed_params["unlisted"] = args.get("unlisted", 0)

    def onFail(self):
        if self.del_dir_on_fail == True:
            file_manager.rmdir(self.temp_dir)
    
    def _fileFromJson(self, json_data):
        from db.File import File

        return File.fromJson(json_data, self.temp_dir)
    
    def _entityFromJson(self, json_data, make_preview = True):
        json_data["extractor_name"] = self.name
        __entity = Entity.fromJson(json_data, self.passed_params)
        # rewrite TODO
        if make_preview == True:
            thumb_result = self.thumbnail(entity=__entity,args=json_data)
            if thumb_result != None:
                __entity.preview = json.dumps(thumb_result)
                __entity.save()

        return __entity
    
    def _collectionFromJson(self, json_data):
        from db.Collection import Collection

        return Collection.fromJson(json_data, self.passed_params)
        
    async def run(self, args):
        pass
    
    async def postRun(self):
        pass
    
    # Typical preview
    def thumbnail(self, entity, args={}):
        from resources.Globals import ThumbnailsRepository
        __FILE = entity.file
        if __FILE == None:
            return None
        
        ext = __FILE.extension
        if args.get("preview_file"):
            ext = utils.get_ext(args.get("preview_file"))
        
        thumb = (ThumbnailsRepository()).getByFormat(ext)
        if thumb == None:
            return None
        
        #thumb_class = thumb(save_dir=__FILE.getDirPath())
        thumb_class = thumb(save_dir=self.temp_dir)
        return thumb_class.run(file=__FILE,params=args)
    
    async def fastGetEntity(self, params, args):
        from db.File import File

        RETURN_ENTITIES = []
        self.setArgs(params)
        EXTRACTOR_RESULTS = await self.execute({})
        for ENTITY in EXTRACTOR_RESULTS.get("entities"):
            RETURN_ENTITIES.append(ENTITY)
            if ENTITY.file != None:
                ENTITY.file.moveTempDir()
        
        await self.postRun()
        return RETURN_ENTITIES
            
    def describe(self):
        return {
            "id": self.name,
            "category": self.category,
            "hidden": getattr(self, "hidden", False),
            "params": getattr(self, "params", {})
        }

    def describeSource(self, INPUT_ENTITY):
        return {"type": "none", "data": {
            "source": None
        }}

    async def execute(self, args):
        EXTRACTOR_RESULTS = None

        try:
            EXTRACTOR_RESULTS = await self.run(args=args)
        except Exception as x:
            logger.logException(x, section="Exctractors")
            self.onFail()

            raise x

        return EXTRACTOR_RESULTS
