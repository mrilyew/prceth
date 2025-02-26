from resources.Globals import importlib, utils, logger
from executables.thumbnail.Base import BaseThumbnail

class Thumbnails:
    def getByFormat(self, input_format):
        for plugin in utils.typicalPluginsList("thumbnail"):
            if plugin == '__init__.py' or plugin == '__pycache__':
                continue

            if plugin.endswith('.py'):
                module_name = f"executables.thumbnail.{plugin[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, BaseThumbnail) and item.name.find('base') == -1:
                            if getattr(item, "hidden", False) == True:
                                continue
                            
                            itemer = item()
                            if itemer.acceptsFormat(input_format):
                                return item
                except ImportError as e:
                    logger.log(f"Error importing {module_name}: {e}")

        return None
