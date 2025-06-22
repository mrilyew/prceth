from app.App import logger
from pathlib import Path
from resources.Consts import consts
from resources.Cached import cached
import importlib

class ExecutableRepository:
    class_type = None
    folder_name = "executables"

    def __category(self):
        if self.class_type == None:
            return ''

        repo_type = self.class_type.__name__ 

        return f"{repo_type.replace('Base', '').lower()}s"

    def doImportRaw(self, folder_name, category, plugin_name):
        __module_name = f'{folder_name}.{category}.{plugin_name}'
        __module = importlib.import_module(__module_name)

        return __module

    def doImport(self, plugin_name):
        try:
            __module = self.doImportRaw(self.folder_name, self.__category(), plugin_name)
            __class = getattr(__module, plugin_name.split(".")[-1])

            if __class.canBeExecuted() == False:
                return None

            return __class
        except Exception as _ex:
            logger.logException(_ex, "Repositories", silent=False)

            raise _ex

    def getByName(self, plugin_name):
        __cached = cached.get(f'{self.__category()}_list')
        if __cached != None:
            __ = plugin_name.split(".")
            for c in __cached:
                print(c.category, c.__name__)
                if c.category == __[0] and c.__name__:
                    return c

        return self.doImport(plugin_name)

    def getList(self, show_hidden: bool = False, search_category: str = None):
        repo_type = self.class_type.__name__

        if cached.get(f'{repo_type}s_list') != None:
            return cached.get(f'{repo_type}s_list')

        __exit = []

        # TODO: Caching
        # TODO: Hiddenness
        __base_path = Path(f"{consts.get('executable')}\\{repo_type}s")
        __plugins = Path(__base_path).rglob('*.py')
        for plugin_file in __plugins:
            if plugin_file.name == '__init__.py' or plugin_file.name == '__pycache__' or plugin_file.name == "Base.py":
                continue

            relative_path = plugin_file.relative_to(__base_path)
            module_name = str(relative_path.with_suffix("")).replace("\\", ".").replace("/", ".")

            if module_name.endswith('.py'):
                __module = self.doImport(module_name.replace(".py", ""))

                __exit.append(__module)
        
        cached[f'{self.self.__category()}_list'] = __exit

        return __exit
