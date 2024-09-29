import os
import importlib
from plugins.BasePlugins import BasePlugin

def load_plugins(folder = 'upload_plugins'):
    plugins = {}
    current_dir = os.path.dirname(__file__)
    
    folder_path = os.path.join(current_dir, folder)
    if os.path.isdir(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith('.py'):
                module_name = f"plugins.{folder}.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    for item_name in dir(module):
                        item = getattr(module, item_name)
                        if isinstance(item, type) and issubclass(item, BasePlugin) and item.name.find('Base') == -1:
                            plugins[item.name] = item
                except ImportError as e:
                    print(f"Error importing {module_name}: {e}")
    return plugins
