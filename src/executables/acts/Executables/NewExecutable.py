from executables.acts.Base.Base import BaseAct
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
            "values": ["act", "extractor", "service", "representation"],
            "assertion": {
                "not_null": True,
            },
        })
        params["category"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["title"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["declare"] = CsvArgument({
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

        template = ""
        template += f"from app.App import logger\n"
        template += f"from {base_class_path} import {base_class}\n"
        template += f"\n"
        template += f"class {title}({base_class}):\n"
        template += f"    category = '{category}'\n"
        template +=  "    docs = {}\n"

        if i.get("is_hidden") == True:
            template += "    hidden = True\n"

        template += "\n"
        template += f"    def declare():\n"
        template +=  "        params = {}\n"

        if i.get('declare') != None:
            for arg in i.get('declare'):
                template += f"        params[\"{arg}\"] = {{}}\n"

        template +=  "        return params\n"
        template += f"\n"
        template +=  "    async def "+execute_name+"(self, i = {}):\n"
        template +=  "        pass\n"

        stream.write(template)
        stream.close()

        return {"path": str(executables_folder_file) + ".py"}
