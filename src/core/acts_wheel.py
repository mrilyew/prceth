from resources.globals import importlib, traceback, logger, consts, os
from acts.Base import BaseAct

def acts_wheel(args, entity_dir, act_name):
    module = importlib.import_module(f'acts.{act_name}')
    instance = getattr(module, act_name)(temp_dir=entity_dir)

    try:
        results = {"result": instance.execute(args=args)}
        results["act_name"] = act_name

        return instance, results
    except Exception as e:
        traceback.print_exc()
        logger.logException(e)
        instance.cleanup_fail()

def acts_list(search_type='all',show_hidden=False):
    acts = []
    current_dir = consts["cwd"] + "\\acts"
    for plugin in os.listdir(current_dir):
        if plugin == '__init__.py' or plugin == '__pycache__':
            continue

        if plugin.endswith('.py'):
            module_name = f"acts.{plugin[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseAct) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        if search_type == "collection" and getattr(item, "allow_type", "all") == "entity" or search_type == "entity" and getattr(item, "allow_type", "all") == "collection":
                            continue
                        
                        acts.append(item())
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
    
    return acts
