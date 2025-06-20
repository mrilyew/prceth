from executables.acts.Base.Base import BaseAct
from resources.Descriptions import descriptions
from resources.Consts import consts
from pathlib import Path
from declarable.ArgumentsTypes import StringArgument, LimitedArgument, CsvArgument
import os

class NewExecutable(BaseAct):
    category = 'Executables'
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["type"] = LimitedArgument({
            "docs": {
                "definition": descriptions.get('__type_of_creating_script'),
                "values": {
                    "act": descriptions.get('__act_title'),
                    "extractor": descriptions.get('__extractor_title'),
                    "service": descriptions.get('__service_title'),
                    "representation": descriptions.get('__representation_title')
                }
            },
            "values": ["act", "extractor", "service", "representation"],
            "assertion": {
                "not_null": True,
            },
        })
        params["category"] = StringArgument({
            "docs": {
                "definition": descriptions.get('__main_category_title')
            },
            "assertion": {
                "not_null": True,
            },
        })
        params["title"] = StringArgument({
            "docs": {
                "definition": descriptions.get('__name_of_the_script')
            },
            "assertion": {
                "not_null": True,
            },
        })
        params["declare"] = CsvArgument({
            "docs": {
                "definition": descriptions.get('__list_of_arguments_divided_by_comma')
            },
            "type": "csv",
            "default": [],
        })

        return params

    async def execute(self, i = {}):
        exec_folder = consts.get("executables")
        exec_folder_by_type = os.path.join(exec_folder, i.get("type") + "s")

        if i.get('type') == 'representation':
            exec_folder = consts.get("representations")
            exec_folder_by_type = exec_folder

        executables_folder_category = os.path.join(exec_folder_by_type, i.get("category"))
        executables_folder_file = os.path.join(executables_folder_category, i.get("title"))

        Path(executables_folder_category).mkdir(exist_ok=True)
        assert Path(executables_folder_file).exists() == False, "script already exists"

        title = i.get("title")
        category = i.get("category")
        execute_name = "execute"

        base_class = f"Base{i.get("type").title()}"
        base_class_path = f"executables.{i.get("type")}s.Base.Base"
        if i.get('type') == 'representation':
            base_class = f"Representation"
            base_class_path = f"{i.get("type")}s.Representation"

        stream = open(str(executables_folder_file) + ".py", "w")

        boilerplate = ""
        boilerplate += f"from app.App import logger\n"
        boilerplate += f"from {base_class_path} import {base_class}\n"
        boilerplate += f"\n"
        boilerplate += f"class {title}({base_class}):\n"
        boilerplate += f"    category = '{category}'\n"
        boilerplate +=  "    docs = {}\n"

        if i.get("is_hidden") == True:
            boilerplate += "    hidden = True\n"

        boilerplate += "\n"
        boilerplate += f"    def declare():\n"
        boilerplate +=  "        params = {}\n"

        if i.get('declare') != None:
            for arg in i.get('declare'):
                boilerplate += f"        params[\"{arg}\"] = {{}}\n"

        boilerplate +=  "        return params\n"
        boilerplate += f"\n"
        boilerplate +=  "    async def "+execute_name+"(self, i = {}):\n"
        boilerplate +=  "        pass\n"

        stream.write(boilerplate)
        stream.close()

        return {"path": str(executables_folder_file) + ".py"}
