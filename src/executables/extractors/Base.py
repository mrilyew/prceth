from resources.Globals import consts, Path, utils, file_manager

class BaseExtractor:
    name = 'base'
    category = 'base'

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def cleanup(self, entity, hash):
        from resources.Globals import storage

        __hash_dir = storage.makeHashDir(hash, only_return=True)
        Path(self.temp_dir).rename(__hash_dir)
        
        entity_file_path = Path(__hash_dir + '\\' + entity.original_name)
        entity_file_path_replace = f'{__hash_dir}\\{str((str(hash) + '.' + entity.format))}'
        entity_file_path.rename(entity_file_path_replace)

    def cleanup_fail(self):
        file_manager.rmdir(self.temp_dir)
    
    async def execute(self, args):
        pass
    
    # Typical preview
    def thumbnail(self, entity, args={}):
        from core.Wheels import thumbnail_wheel

        ext = entity.format
        if args.hasPreview():
            ext = utils.get_ext(args.another_file)
        
        thumb = thumbnail_wheel(ext)
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
