from resources.Globals import os, logger, consts, Path
from executables.acts.Base.Base import BaseAct

class NewExecutable(BaseAct):
    name = 'NewExecutable'
    category = 'new'
    docs = {
        "description": {
            "name": {
                "ru": "Новый скрипт",
                "en": "New executable"
            },
            "definition": {
                "ru": "Создаёт новый пустой скрипт по названию и категории",
                "en": "Creates new empty script by name and category"
            }
        }
    }

    def declare():
        params = {}
        params["type"] = {
            "docs": {
                "definition": {
                    "ru": "Тип создаваемого скрипта",
                    "en": "Type of new script",
                },
                "values": {
                    "act": {
                        "ru": "Скрипт выполнения какого-либо действия",
                        "en": "Script for doing some actions"
                    },
                    "extractor": {
                        "ru": "Скрипт для извлечения какой-либо информации",
                        "en": "Script for information extracting"
                    },
                    "service": {
                        "ru": "Скрипт, выполняющийся раз в некоторое время",
                        "en": "Script that runs sometimes"
                    }
                }
            },
            "type": "array",
            "values": ["act", "extractor", "service"],
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["category"] = {
            "docs": {
                "definition": {
                    "ru": "Основная категория скрипта",
                    "en": "Main category of script",
                }
            },
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["title"] = {
            "docs": {
                "definition": {
                    "ru": "Название скрипта",
                    "en": "Name of the script",
                }
            },
            "type": "string",
            "assertion": {
                "assert_not_null": True,
            },
        }
        params["is_hidden"] = {
            "docs": {
                "definition": {
                    "ru": "Добавить параметр 'hidden' к скрипту",
                    "en": "Add 'hidden' param to script",
                }
            },
            "type": "bool",
            "default": False,
            "assertion": {
                "assert_not_null": True,
            },
        }

        return params

    async def execute(self, args={}):
        executables_folder = consts.get("executable")
        executables_folder_sub = os.path.join(executables_folder, self.passed_params.get("type") + "s")
        executables_folder_category = os.path.join(executables_folder_sub, self.passed_params.get("category"))
        executables_folder_file = os.path.join(executables_folder_category, self.passed_params.get("title"))

        Path(executables_folder_category).mkdir(exist_ok=True)
        assert Path(executables_folder_file).exists() == False, "script already exists"

        base_class = f"Base{self.passed_params.get("type").title()}"
        new_class_name = self.passed_params.get("title")
        new_class_category = self.passed_params.get("category")
        execute_name = "execute"

        if self.passed_params.get("type") == "extractor":
            execute_name = "run"

        stream = open(str(executables_folder_file) + ".py", "w")
        wr  = f"from resources.Globals import os, logger, asyncio, consts, config, Path, utils, file_manager, json, often_params\n"
        wr += f"from executables.{self.passed_params.get("type")}s.Base.Base import {base_class}\n\n"
        wr += f"class {new_class_name}({base_class}):\n"
        wr += f"    name = '{new_class_name}'\n"
        wr += f"    category = '{new_class_category}'\n"
        wr +=  "    docs = {}\n"
        if self.passed_params.get("is_hidden") == True:
            wr += "    hidden = True\n"
        wr += "\n"
        wr += f"    def declare():\n"
        wr +=  "        params = {}\n\n"
        wr +=  "        return params\n\n"
        wr +=  "    async def "+execute_name+"(self, args={}):\n"
        wr +=  "        pass\n"

        stream.write(wr)
        stream.close()

        return {"path": str(executables_folder_file) + ".py"}
