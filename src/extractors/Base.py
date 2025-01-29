from resources.globals import consts, Path, utils, file_manager

class BaseExtractor:
    name = 'base'
    category = 'base'

    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir

    def cleanup(self, entity):
        entity_dir = f'{consts['cwd']}\\storage\\collections\\{str(entity.id)}'
        Path(self.temp_dir).rename(entity_dir)

        entity_file_path = Path(entity_dir + '\\' + entity.original_name)
        entity_file_path_replace = f'{entity_dir}\\{str((str(entity.id) + '.' + entity.format))}'
        entity_file_path.rename(entity_file_path_replace)

    def cleanup_fail(self):
        file_manager.rmdir(self.temp_dir)
    
    def execute(self, args):
        pass
    
    # Typical preview
    def thumbnail(self, entity, args={}):
        from core.wheels import thumbnail_wheel
        ext   = entity.format
        if "another_file" in args:
            ext = utils.get_ext(args.get("another_file"))
        
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
