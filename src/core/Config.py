from resources.Globals import json, os, consts
from resources.DefaultSettings import DefaultSettings

class Config():
    def __init__(self, file_name: str = 'config.json', fallback = DefaultSettings):
        self.default_settings = fallback
        self.path = f"{consts.get('cwd')}/storage/settings/{file_name}"
        self.__load_path(self.path)
        self.__pass_declarable()

        if file_name == "config.json":
            self.__set_consts()
        # о даа я готов смотреть сериальчики

    def __pass_declarable(self):
        from resources.Globals import DeclarableArgs

        is_free_settings = self.default_settings == None

        self.declared_settings = DeclarableArgs(self.default_settings, self.json_values, "pass", is_free_settings)
        self.out_params = self.declared_settings.dict()
    
    def __load_path(self, path):
        if not os.path.exists(self.path):
            __temp_config_write_stream = open(self.path, 'w', encoding='utf-8')
            json.dump({}, __temp_config_write_stream)
            __temp_config_write_stream.close()
            # logger.log("Config", "success", "Created config file")

        self.file = open(self.path, 'r+', encoding='utf-8')
        try:
            self.json_values = json.load(self.file)
        except json.JSONDecodeError as __exc:
            self.file.write("{}")
            self.json_values = dict()
            # logger.logException(input_exception=__exc,section="Config")

    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def __update_file(self):
        self.file.seek(0)
        json.dump(self.json_values, self.file, indent=4)
        self.file.truncate()

    def __set_consts(self):
        consts["storage"] = self.get("storage.path").replace("?cwd?", os.getcwd())
        consts["tmp"] = os.path.join(consts.get('storage'), "tmp")
        consts["binary"] = os.path.join(consts.get('storage'), "binary")

    def get(self, option: str, default: str = None):
        return self.out_params.get(option, default)
    
    def set(self, option: str, value: str):
        if value == None:
            del self.json_values[option]
        else:
            self.json_values[option] = value

        self.__update_file()
        self.__pass_declarable()

    def reset(self):
        self.file.seek(0)
        self.file.write("{}")
        self.file.truncate()
        self.out_params = {}

config = Config()
env = Config(file_name="env.json",fallback=None)
