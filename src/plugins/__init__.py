import os
import importlib
from plugins.BasePlugins import BasePlugin

def load_plugins(folder = 'upload_plugins'):
    if folder == None:
        folder = 'upload_plugins'
    
    plugins = {}
    current_dir = os.path.dirname(__file__)
    folder_path = current_dir + '\\' + folder
    # Checking main folder
    if os.path.isdir(folder_path):
        # Getting categories
        for sub_folder in os.listdir(folder_path):
            if sub_folder == '__init__.py' or sub_folder == '__pycache__':
                continue
            
            # Getting plugins
            for plugin in os.listdir(folder_path + '\\' + sub_folder):
                if plugin.endswith('.py'):
                    module_name = f"plugins.{folder}.{sub_folder}.{plugin[:-3]}"
                    try:
                        module = importlib.import_module(module_name)
                        for item_name in dir(module):
                            item = getattr(module, item_name)
                            if isinstance(item, type) and issubclass(item, BasePlugin) and item.name.find('Base') == -1:
                                plugins[item.name] = item
                    except ImportError as e:
                        print(f"Error importing {module_name}: {e}")
    
    return plugins
