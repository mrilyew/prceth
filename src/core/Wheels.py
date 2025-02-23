from resources.Globals import importlib, traceback, logger, consts, os, time
from executables.services.Base import BaseService
from executables.extractors.Base import BaseExtractor
from executables.acts.Base import BaseAct
from executables.thumbnail.Base import BaseThumbnail
from executables.acts.AExtractMetadata import AExtractMetadata
from executables.acts.AAdditionalMetadata import AAdditionalMetadata

def __typical_plugins_list(folder):
    dir = f"{consts["executable"]}\\{folder}"

    return os.listdir(dir)

def acts_wheel(args, entity_dir, act_name):
    module = importlib.import_module(f'executables.acts.{act_name}')
    instance = getattr(module, act_name)(temp_dir=entity_dir)

    try:
        results = {"result": instance.execute(args=args)}
        results["act_name"] = act_name

        return instance, results
    except Exception as e:
        logger.logException(e)
        instance.cleanup_fail()

def acts_list(search_type='all',show_hidden=False):
    __exit = []
    for __plugin_name in __typical_plugins_list("acts"):
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

async def extractor_wheel(args, entity_dir, extractor_name):
    module = importlib.import_module(f'executables.extractors.{extractor_name}')
    instance = getattr(module, extractor_name)(temp_dir=entity_dir)

    try:
        results = await instance.execute(args=args)

        return instance, results
    except Exception as e:
        logger.logException(e, section=f"Extractors | {extractor_name}")
        instance.cleanup_fail()
        raise 

def extractor_find(extractor_name):
    try:
        module = importlib.import_module(f'executables.extractors.{extractor_name}')
        __class = getattr(module, extractor_name)
        if __class.category == "template":
            return None
        
        return __class
    except Exception:
        return None

def extractor_list(show_hidden=False):
    __exit = []
    for plugin in __typical_plugins_list("extractors"):
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
                print(f"Error importing {module_name}: {e}")
    
    return __exit

def service_wheel(args, service_name):
    module = importlib.import_module(f'executables.services.{service_name}')
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
    __exit = []
    for plugin in __typical_plugins_list("services"):
        if plugin == '__init__.py' or plugin == '__pycache__':
            continue

        if plugin.endswith('.py'):
            module_name = f"executables.services.{plugin[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BaseService) and item.name.find('base') == -1:
                        if not show_hidden and getattr(item, "hidden", False):
                            continue

                        __exit.append(item())
            except ImportError as e:
                print(f"Error importing {module_name}: {e}")
    
    return __exit

def metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = AExtractMetadata()
    res = md.execute(args=ps)

    return res

def thumbnail_wheel(input_format):
    for plugin in __typical_plugins_list("thumbnail"):
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
                print(f"Error importing {module_name}: {e}")

    return None

def additional_metadata_wheel(input_file):
    ps = dict()
    ps["type"] = "arr"
    ps["input_file"] = input_file

    md = AAdditionalMetadata()
    res = md.execute(args=ps)

    return res
