from resources.globals import consts, Path, utils

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
        utils.rmdir(self.temp_dir)
    
    def execute(self, args):
        pass
