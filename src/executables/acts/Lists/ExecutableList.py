from resources.Globals import os, logger, asyncio, consts, config, Path, utils, ServicesRepository, ExtractorsRepository, ActsRepository, often_params
from executables.acts.Base.Base import BaseAct

class ExecutableList(BaseAct):
    name = 'ExecutableList'
    category = 'Lists'
    docs = {}

    def declare():
        params = {}
        params["show_hidden"] = {
            "type": "bool",
            "default": False,
            "docs": {
                "definition": {
                    "ru": "Показывать скрытые скрипты",
                    "en": "Show hidden executables",
                }
            },
        }
        params["category"] = often_params.get("category_of_search")
        params["return_raw"] = often_params.get("return_raw")
        params["type"] = {
            "type": "array",
            "values": ["acts", "extractors", "services"],
            "docs": {
                "definition": {
                    "ru": "Тип скриптов для поиска",
                    "en": "Search script type",
                },
                "values": {
                    "acts": {
                        "ru": "Выполняющие",
                        "en": "Acts"
                    },
                    "extractors": {
                        "ru": "Экстракторы",
                        "en": "Extractors"
                    },
                    "services": {
                        "ru": "Сервисы",
                        "en": "Services"
                    },
                }
            },
            "assertion": {
                "assert_not_null": True,
            }
        }
        return params

    async def execute(self, args={}):
        __show_hidden = self.passed_params.get("show_hidden")
        __type = self.passed_params.get("type")
        __return_raw = self.passed_params.get("return_raw")
        __category = self.passed_params.get("category")

        lists = None
        final_lists = []
        match(__type):
            case "acts":
                lists = ActsRepository().getList(show_hidden=__show_hidden,search_category=__category)
            case "extractors":
                lists = (ExtractorsRepository()).getList(show_hidden=__show_hidden,search_category=__category)
            case "services":
                lists = (ServicesRepository()).getList(show_hidden=__show_hidden,search_category=__category)
       
        for exec in lists:
            if __return_raw == False:
                final_lists.append(exec.describe())
            else:
                final_lists.append(exec)
        
        return final_lists
