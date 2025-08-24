from resources.Cached import cached
from resources.Consts import consts
from typing import List, Type
from pathlib import Path
import importlib

class Findable():
    self_name = "Executable"

    @classmethod
    def findByNameRaw(cls, category, title, sub = None, any = False)->Type["Findable"]:
        folder = "executables"

        __module_name = f'{folder}.list.{category}.{title}'
        __module = importlib.import_module(__module_name)
        __class = getattr(__module, "Implementation", None)
        if __class == None:
            return None

        if sub != None:
            __class = __class.get_submodule("Acts", sub)

        if any == False and __class.self_name != cls.self_name:
            return None

        return __class

    @classmethod
    def findByName(cls, name, any = False)->Type["Findable"]:
        __module = None
        _name_parts = name.split(".")
        _category = _name_parts[0]
        _title = _name_parts[1]
        _sub = None
        if len(_name_parts) > 2:
            _sub = _name_parts[2]

        try:
            __module = cls.findByNameRaw(_category, _title, _sub, any)
        except Exception as e:
            return None

        if getattr(__module, 'canBeExecuted', None) == None or __module.canBeExecuted() == False:
            return None

        return __module

    @classmethod
    def findAll(cls)->List[Type["Findable"]]:
        self_name_but_correct = cls.self_name.lower() + "s"
        output = []

        if cached.get(f'{self_name_but_correct}_list') != None:
            return cached.get(f'{self_name_but_correct}_list')

        executables_dir = consts.get('executables')
        list_dir = Path(f"{executables_dir}\\list")
        plugins_list = Path(list_dir).rglob('*__init__.py')
        for plugin_file in plugins_list:
            plugin_name = plugin_file.name
            if plugin_name in ['', '__pycache__', 'Base.py']:
                continue

            relative_path = plugin_file.relative_to(list_dir)
            module_name = str(relative_path.with_suffix("")).replace("\\", ".").replace("/", ".")

            if plugin_name.endswith('.py'):
                __module = cls.findByName(module_name)
                if __module != None:
                    output.append(__module)

        cached[f'{self_name_but_correct}_list'] = output

        return output
