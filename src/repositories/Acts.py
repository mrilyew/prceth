from resources.Globals import importlib, utils, logger
from executables.acts.Base import BaseAct

class Acts:
    def run(self, args, entity_dir, act_name):
        module = importlib.import_module(f'executables.acts.{act_name}')
        instance = getattr(module, act_name)(temp_dir=entity_dir)

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
            __class = getattr(module, act_name)
            if __class.category == "template" or __class.category == "base":
                return None
            
            return __class
        except Exception:
            return None

    def getList(self, search_type='all',show_hidden=False):
        __exit = []
        for __plugin_name in utils.typicalPluginsList("acts"):
            if __plugin_name == '__init__.py' or __plugin_name == '__pycache__':
                continue

            if __plugin_name.endswith('.py'):
                __module_name = f"executables.acts.{__plugin_name[:-3]}"
                try:
                    module = importlib.import_module(__module_name)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, BaseAct) and item.name.find('base') == -1:
                            if not show_hidden and getattr(item, "hidden", False):
                                continue

                            if search_type == "collection" and getattr(item, "allow_type", "all") == "entity" or search_type == "entity" and getattr(item, "allow_type", "all") == "collection":
                                continue
                            
                            __exit.append(item())
                except ImportError as e:
                    print(f"Error importing {__module_name}: {e}")
        
        return __exit
