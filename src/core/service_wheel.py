from resources.globals import importlib, traceback, logger, consts, os, time
from services.Base import BaseService

def service_wheel(args, service_name):
    module = importlib.import_module(f'services.{service_name}')
    instance = getattr(module, service_name)(args=args)

    try:
        instance.start()
    except Exception as e:
        traceback.print_exc()
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
