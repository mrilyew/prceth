from resources.globals import importlib, traceback, logger, consts, os
from extractors.Base import BaseExtractor

def extractor_wheel(args, entity_dir, extractor_name):
    module = importlib.import_module(f'extractors.{extractor_name}')
    instance = getattr(module, extractor_name)(temp_dir=entity_dir)

    try:
        results = instance.execute(args=args)
        results["extractor_name"] = extractor_name

        return instance, results
    except Exception as e:
        traceback.print_exc()
        logger.logException(e)
        instance.cleanup_fail()

def extractor_list(show_hidden=False):
    extractors = []
    current_dir = consts["cwd"] + "\\extractors"
    for plugin in os.listdir(current_dir):
        if plugin == '__init__.py' or plugin == '__pycache__':
            continue

        if plugin.endswith('.py'):
            module_name = f"extractors.{plugin[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseExtractor) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        extractors.append(item())
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
    
    return extractors
