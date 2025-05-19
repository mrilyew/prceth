often_definitions = {}
often_definitions["count"] = {
    "ru": "Число получаемых элементов",
    "en": "Pagination offset number",
}
often_definitions["offset"] = {
    "ru": "Числовой отступ для пагинации",
    "en": "Pagination offset number",
}
often_definitions["return_raw"] = {
    "ru": "Вернуть внутренние объекты",
    "en": "Return internal objects",
}
often_definitions["category_of_search"] = {
    "ru": "Категория поиска",
    "en": "Search category",
}
often_definitions["path_to_file"] = {
    "ru": "Путь к файлу",
    "en": "Path to file",
}

often_params = {}
often_params["count_default_10"] = {
    "type": "int",
    "default": 10,
    "docs": {
        "definition": often_definitions.get("count")
    },
    "assertion": {
        "assert_not_null": True,
    },
}
often_params["offset_default_0"] = {
    "type": "int",
    "default": 0,
    "docs": {
        "definition": often_definitions.get("offset")
    },
    "assertion": {
        "assert_not_null": True,
    },
}
often_params["return_raw"] = {
    "type": "bool",
    "default": False,
    "docs": {
        "definition": often_definitions.get("return_raw")
    },
}
often_params["category_of_search"] = {
    "type": "string",
    "default": None,
    "docs": {
        "definition": often_definitions.get("category_of_search")
    },
}
often_params["path"] = {
    "type": "string",
    "default": None,
    "docs": {
        "definition": often_definitions.get("path_to_file")
    },
}
