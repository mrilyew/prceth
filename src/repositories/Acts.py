from resources.Globals import importlib, utils, logger
from executables.acts.Base.Base import BaseAct

class Acts:
    def run(self, args, entity_dir, act_name):
        module = importlib.import_module(f'executables.acts.{act_name}')
        instance = getattr(module, act_name.split(".")[-1])(temp_dir=entity_dir)

        try:
            results = {"result": instance.execute(args=args)}
            results["act_name"] = act_name

            return instance, results
        except Exception as e:
            logger.logException(e)
            instance.cleanup_fail()
    
    def getByName(self, act_name):
        try:
            module = importlib.import_module(f'executables.acts.{act_name}')
            __class = getattr(module, act_name.split(".")[-1])
            if __class.category == "template" or __class.category == "base":
                return None
            
            return __class
        except Exception:
            return None

    def getList(self, search_type:str = 'all',show_hidden:bool = False):
        __exit = []
        def __import(plugin_name):
            module_name = plugin_name
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseAct) and item.name.find('base') == -1 and item.name.find('Template') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        if getattr(item, "accepts", "all") == "entity":
                            if search_type == "collection" or search_type == "string":
                                continue

                        if getattr(item, "accepts", "all") == "collection":
                            if search_type == "entity" or search_type == "string":
                                continue

                        if getattr(item, "accepts", "all") == "string":
                            if search_type == "entity" or search_type == "collection":
                                continue

                        __exit.append(item())
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
        
        for plugin in utils.getExecutableList("acts"):
            __import(f"executables.acts.{plugin}")
        
        return __exit
