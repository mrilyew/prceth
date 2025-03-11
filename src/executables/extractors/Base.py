from resources.Globals import consts, Path, utils, file_manager, json, logger
from db.Entity import Entity

class BaseExtractor:
    name = 'base'
    category = 'template'
    passed_params = {}

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def passParams(self, args):
        self.passed_params["display_name"] = args.get("display_name", None)
        self.passed_params["description"] = args.get("description", None)
        self.passed_params["is_hidden"] = args.get("is_hidden", None)

    def saveAsEntity(self, __EXECUTE_RESULT):
        FINAL_ENTITY = Entity()
        if __EXECUTE_RESULT.hasHash() == False:
            __hash = utils.getRandomHash(32)
        else:
            __hash = __EXECUTE_RESULT.hash
        
        indexation_content_ = __EXECUTE_RESULT.indexation_content
        entity_internal_content_ = __EXECUTE_RESULT.entity_internal_content

        FINAL_ENTITY.hash = __hash
        if __EXECUTE_RESULT.hasInternalContent():
            FINAL_ENTITY.entity_internal_content = json.dumps(entity_internal_content_)
        else:
            FINAL_ENTITY.entity_internal_content = json.dumps(indexation_content_)
        
        if __EXECUTE_RESULT.main_file == None:
            FINAL_ENTITY.type = 0
        else:
            FINAL_ENTITY.type = 1
        
        if __EXECUTE_RESULT.isUnlisted() or self.passed_params.get("is_hidden") == True:
            FINAL_ENTITY.unlisted = 1
        
        FINAL_ENTITY.file_id = __EXECUTE_RESULT.main_file.id
        FINAL_ENTITY.extractor_name = self.name
        if self.passed_params.get("display_name") != None:
            FINAL_ENTITY.display_name = self.passed_params["display_name"]
        else:
            if __EXECUTE_RESULT.main_file == None:
                FINAL_ENTITY.display_name = "N/A"
            else:
                FINAL_ENTITY.display_name = __EXECUTE_RESULT.main_file.upload_name
        
        if self.passed_params.get("description") != None:
            FINAL_ENTITY.description = self.passed_params["description"]
        if __EXECUTE_RESULT.hasSource():
            FINAL_ENTITY.source = __EXECUTE_RESULT.source
        if __EXECUTE_RESULT.hasIndexationContent():
            #FINAL_ENTITY.indexation_content = json.dumps(indexation_content_) # remove
            FINAL_ENTITY.indexation_content_string = str(utils.json_values_to_string(indexation_content_)).replace('None', '').replace('  ', ' ')
        else:
            FINAL_ENTITY.indexation_content_string = json.dumps(entity_internal_content_)
        
        FINAL_ENTITY.save()

        return FINAL_ENTITY

    # Does nothing :D
    def saveToDirectory(self, __EXECUTE_RESULT):
        pass

    def onFail(self):
        file_manager.rmdir(self.temp_dir)

    async def run(self, args):
        pass
    
    async def postRun(self):
        pass
    
    # Typical preview
    def thumbnail(self, entity, args={}):
        from resources.Globals import ThumbnailsRepository
        __FILE = entity.file

        ext = __FILE.extension
        if args.hasPreview():
            ext = utils.get_ext(args.another_file)
        
        thumb = (ThumbnailsRepository()).getByFormat(ext)
        if thumb == None:
            return None
        
        thumb_class = thumb(save_dir=__FILE.getDirPath())
        return thumb_class.run(file=__FILE,params=args)
    
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
