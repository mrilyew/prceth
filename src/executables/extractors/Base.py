from resources.Globals import consts, Path, utils, file_manager, json
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

    def saveAsEntity(self, __EXECUTE_RESULT):
        FINAL_ENTITY = Entity()
        if __EXECUTE_RESULT.hasHash() == False:
            __hash = utils.getRandomHash(32)
        else:
            __hash = __EXECUTE_RESULT.hash
        
        json_ = __EXECUTE_RESULT.json_info
        summary_ = __EXECUTE_RESULT.summary # both
        FINAL_ENTITY.hash = __hash
        FINAL_ENTITY.original_name = __EXECUTE_RESULT.original_name
        FINAL_ENTITY.filesize = __EXECUTE_RESULT.filesize
        if __EXECUTE_RESULT.no_file == False:
            FINAL_ENTITY.format = __EXECUTE_RESULT.format
            FINAL_ENTITY.dir_filesize = file_manager.getFolderSize(self.temp_dir)
        else:
            FINAL_ENTITY.format = "json"
            FINAL_ENTITY.dir_filesize = 0
            FINAL_ENTITY.type = 1
            FINAL_ENTITY.type_sub = json.dumps(summary_)
        
        if __EXECUTE_RESULT.isUnlisted():
            FINAL_ENTITY.unlisted = 1
        
        FINAL_ENTITY.extractor_name = self.name
        if self.passed_params.get("display_name") != None:
            FINAL_ENTITY.display_name = self.passed_params["display_name"]
        else:
            FINAL_ENTITY.display_name = __EXECUTE_RESULT.original_name
        if self.passed_params.get("description") != None:
            FINAL_ENTITY.description = self.passed_params["description"]
        if __EXECUTE_RESULT.hasSource():
            FINAL_ENTITY.source = __EXECUTE_RESULT.source
        if __EXECUTE_RESULT.hasJsonInfo():
            FINAL_ENTITY.json_info = json.dumps(json_)
            FINAL_ENTITY.index_content = str(utils.json_values_to_string(json_)).replace('None', '').replace('  ', ' ')
        
        FINAL_ENTITY.save()

        return FINAL_ENTITY

    def moveDestinationDirectory(self, entity):
        from resources.Globals import storage

        __hash_dir = storage.makeHashDir(entity.hash, only_return=True)
        Path(self.temp_dir).rename(__hash_dir)
        
        entity_file_path = Path(__hash_dir + '\\' + entity.original_name)
        entity_file_path_replace = f'{__hash_dir}\\{str((str(entity.hash) + '.' + entity.format))}'
        entity_file_path.rename(entity_file_path_replace)
    
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
        
        ext = entity.format
        if args.hasPreview():
            ext = utils.get_ext(args.another_file)
        
        thumb = (ThumbnailsRepository()).getByFormat(ext)
        if thumb == None:
            return None
        
        thumb_class = thumb(save_dir=entity.getDirPath())
        return thumb_class.run(entity=entity,params=args)
    
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

