from resources.globals import json, os

class Settings():
    def __init__(self, file_name = 'main.json'):
        self.default_settings = {
            "ui.lang": {
                "type": "string",
                "default_value": 'ru',
            }
        }

        self.settings_path = os.getcwd() + '/storage/settings/' + file_name
        if not os.path.exists(self.settings_path):
            temp_stream = open(self.settings_path, 'w', encoding='utf-8')
            json.dump({}, temp_stream)
            temp_stream.close()
            
            print('Settings | Created settings file')

        self.file = open(self.settings_path, 'r+', encoding='utf-8')
        try:
            self.data = json.load(self.file)
        except json.JSONDecodeError:
            self.file.write("{}")
            self.data = dict()

            print('Settings | Error opening settings file')
    
    def __del__(self):
        try:
            self.file.close()
        except AttributeError:
            pass

    def get(self, setting, default = None):
        if setting in self.data:
            setting_value = self.data[setting]
            return setting_value
        
        if setting in self.default_settings:
            temp_setting = self.default_settings[setting]

            return temp_setting['default_value']
        
        if default != None:
            return default
    
    def set(self, setting, value):
        if value == None:
            del self.data[setting]
        else:
            self.data[setting] = value

        self.file.seek(0)
        json.dump(self.data, self.file, indent=4)
        self.file.truncate()

    def reset(self):
        self.file.seek(0)
        self.file.write("{}")
        self.file.truncate()
        self.data = {}

settings = Settings()
