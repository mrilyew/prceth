from resources.Globals import importlib, utils, logger, Path, consts
from executables.extractors.Base.Base import BaseExtractor

class Extractors:
    def getByName(self, extractor_name):
        try:
            module = importlib.import_module(f'executables.extractors.{extractor_name}')
            __class = getattr(module, extractor_name.split(".")[-1])
            if __class.isRunnable() == False:
                return None
            
            return __class
        except ModuleNotFoundError:
            return None
        except Exception as ee:
            logger.logException(ee, "Extractors", silent=False)
            return None

    def getList(self, show_hidden=False):
        __exit = []
        def __import(plugin_name):
            module_name = plugin_name
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseExtractor) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue
                        
                        __i = item()
                        __i.recursiveDeclare()

                        __exit.append(__i)
            except ModuleNotFoundError:
                return None
            except ImportError as e:
                logger.log(message=f"Error importing {module_name}: {e}")

        for plugin in utils.getExecutableList("extractors"):
            __import(f"executables.extractors.{plugin}")
        
        return __exit
