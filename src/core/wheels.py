from resources.globals import importlib, traceback, logger, consts, os, time
from services.Base import BaseService
from extractors.Base import BaseExtractor
from acts.Base import BaseAct
from acts.metadata import metadata
from acts.additional_metadata import additional_metadata

def acts_wheel(args, entity_dir, act_name):
    module = importlib.import_module(f'acts.{act_name}')
    instance = getattr(module, act_name)(temp_dir=entity_dir)

    try:
        results = {"result": instance.execute(args=args)}
        results["act_name"] = act_name

        return instance, results
    except Exception as e:
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

def extractor_wheel(args, entity_dir, extractor_name):
    module = importlib.import_module(f'extractors.{extractor_name}')
    instance = getattr(module, extractor_name)(temp_dir=entity_dir)

    try:
        results = instance.execute(args=args)
        results["extractor_name"] = extractor_name

        return instance, results
    except Exception as e:
        logger.logException(e)
        instance.cleanup_fail()
        raise

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


def service_wheel(args, service_name):
    module = importlib.import_module(f'services.{service_name}')
    instance = getattr(module, service_name)(args=args)

    try:
        instance.start()
    except Exception as e:
        logger.logException(e)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        instance.stop()

def services_list(show_hidden=False):
    services = []
    current_dir = consts["cwd"] + "\\services"
    for plugin in os.listdir(current_dir):
        if plugin == '__init__.py' or plugin == '__pycache__':
            continue

        if plugin.endswith('.py'):
            module_name = f"services.{plugin[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseService) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        services.append(item())
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
    
    return services

def metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = metadata()
    res = md.execute(args=ps)

    return res

def additional_metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = additional_metadata()
    res = md.execute(args=ps)

    return res
