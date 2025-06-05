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
often_definitions["xml_code"] = {
    "ru": "XML код",
    "en": "XML code",
}
often_definitions["save_original_xml"] = {
    "ru": "Сохранять оригинальный XML",
    "en": "Save original XML",
}
often_definitions["simple_source"] = {
    "ru": "Источник",
    "en": "Source",
}
often_definitions["xml_parsed_code"] = {
    "ru": "Уже спаршенный xml если таковой имеется",
    "en": "Already parsed xml if you have it",
}
often_definitions["suggested_name"] = {
    "ru": "Предлагаемое название записи",
    "en": "Suggested name of ContentUnit",
}

often_params = {}
often_params["count_default_10"] = {
    "type": "int",
    "default": 10,
    "docs": {
        "definition": often_definitions.get("count")
    },
    "assertion": {
        "not_null": True,
    },
}
often_params["offset_default_0"] = {
    "type": "int",
    "default": 0,
    "docs": {
        "definition": often_definitions.get("offset")
    },
    "assertion": {
        "not_null": True,
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
often_params["xml_explain"] = {
    "docs": {
        "definition": often_definitions.get("xml_code")
    },
    "type": "string",
}
often_params["xml_parsed_explain"] = {
    "docs": {
        "definition": often_definitions.get("xml_parsed_code")
    },
    "type": "object",
}
often_params["save_original_xml"] = {
    "docs": {
        "definition": often_definitions.get("save_original_xml")
    },
    "default": False,
    "type": "bool",
    "assertion": {
        "not_null": True,
    },
}
often_params["simple_source"] = {
    "docs": {
        "definition": often_definitions.get("simple_source")
    },
    "type": "string",
    "assertion": {
        "not_null": True,
    },
}
often_params["suggested_name"] = {
    "docs": {
        "definition": often_definitions.get("suggested_name")
    },
    "type": "string",
    "assertion": {
        "not_null": True,
    },
}
