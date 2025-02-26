from resources.Globals import importlib, utils, logger
from executables.extractors.Base import BaseExtractor

class Extractors:
    def getByName(self, extractor_name):
        try:
            module = importlib.import_module(f'executables.extractors.{extractor_name}')
            __class = getattr(module, extractor_name)
            if __class.category == "template":
                return None
            
            return __class
        except Exception:
            return None

    def getList(self, show_hidden=False):
        __exit = []
        for plugin in utils.typicalPluginsList("extractors"):
            if plugin == '__init__.py' or plugin == '__pycache__':
                continue

            if plugin.endswith('.py'):
                module_name = f"executables.extractors.{plugin[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, BaseExtractor) and item.name.find('base') == -1:
                            if not show_hidden and getattr(item, "hidden", False):
                                continue

                            __exit.append(item())
                except ImportError as e:
                    logger.log(f"Error importing {module_name}: {e}")
        
        return __exit
