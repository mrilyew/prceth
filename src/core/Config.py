from resources.Globals import json, os, consts
from resources.literal.DefaultSettings import DefaultSettings

class Config():
    def __init__(self, file_name: str = 'config.json'):
        self.default_settings = DefaultSettings
        path_to_config = f"{consts['cwd']}/storage/settings/{file_name}"
        # path_to_config = f"your/custom/path/..."

        self.path = path_to_config
        
        if not os.path.exists(self.path):
            __temp_config_write_stream = open(self.path, 'w', encoding='utf-8')
            json.dump({}, __temp_config_write_stream)
            __temp_config_write_stream.close()
            # logger.log("Config", "success", "Created config file")

        self.file = open(self.path, 'r+', encoding='utf-8')
        try:
            self.data = json.load(self.file)
        except json.JSONDecodeError as __exc:
            self.file.write("{}")
            self.data = dict()

            # logger.logException(input_exception=__exc,section="Config")

        self.__post_init()
    
    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def __update_file(self):
        self.file.seek(0)
        json.dump(self.data, self.file, indent=4)
        self.file.truncate()

    def __post_init(self):
        consts["storage"] = self.get("storage.path").replace("?cwd?", os.getcwd())
        consts["tmp"] = os.path.join(consts["storage"], "tmp")
        consts["binary"] = os.path.join(consts["storage"], "binary")

    def get(self, option: str, default: str = None):
        # if option is passed in settings, return it
        if option in self.data:
            setting_value = self.data[option]
            return setting_value
        
        # if option contains in preset settings
        if option in self.default_settings:
            __temp_preset_option = self.default_settings[option]

            return __temp_preset_option['default_value']
        
        # so return passed default
        if default != None:
            return default
    
    def set(self, option: str, value: str):
        if value == None:
            del self.data[option]
        else:
            self.data[option] = value

        self.__update_file()

    def reset(self):
        self.file.seek(0)
        self.file.write("{}")
        self.file.truncate()
        self.data = {}

config = Config()
env = Config(file_name="env.json")
