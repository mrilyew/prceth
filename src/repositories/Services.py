from resources.Globals import importlib, utils, logger, time
from executables.services.Base.Base import BaseService

class Services:
    def getByName(self, service_name):
        try:
            module = importlib.import_module(f'executables.services.{service_name}')
            __class = getattr(module, service_name.split(".")[-1])
            if __class.isRunnable() == False:
                return None
            
            return __class
        except ModuleNotFoundError:
            return None
        except Exception as ee:
            logger.logException(ee, "Executables", silent=False)
            return None

    def getList(self, show_hidden: bool = False, search_category: str = None):
        __exit = []
        def __import(plugin_name):
            module_name = plugin_name
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseService) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        if search_category != None and search_category != item.category:
                            continue

                        __exit.append(item())
            except ImportError as e:
                logger.log(message=f"Error importing {module_name}: {e}")

            
        for plugin in utils.getExecutableList("services"):
            __import(f"executables.services.{plugin}")
        
        return __exit
