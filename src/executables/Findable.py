from resources.Cached import cached
from resources.Consts import consts
from typing import List, Type
from pathlib import Path
import importlib

class Findable():
    self_name = "Executable"
    cached_lists = {}

    @classmethod
    def findByNameRaw(cls, category, title, sub = None, any = False)->Type["Findable"]:
        folder = "executables"

        try:
            module_name = f'{folder}.list.{category}.{title}'
            module = importlib.import_module(module_name)
            if module == None:
                return None

            class_object = getattr(module, "Implementation", None)
            sub_object = None

            assert class_object != None

            if sub != None:
                sub_object = class_object.get_submodule("Acts", sub)
            else:
                if any == False:
                    assert class_object.self_name != cls.self_name

            if sub_object != None:
                return sub_object(class_object)

            return class_object()
        except AssertionError:
            return None

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
