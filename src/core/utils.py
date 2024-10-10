import sys
import random
import json
from resources.consts import consts
from pathlib import Path

class Utils():
    def parse_args(self):
        args = sys.argv
        parsed_args = {}
        key = None
        for arg in args[1:]:
            if arg.startswith('--'):
                if key:
                    parsed_args[key] = True
                key = arg[2:]
                parsed_args[key] = True
            #elif arg.startswith('-'):
            #    if key:
            #        parsed_args[key] = True
            #    key = arg[1:]
            #    parsed_args[key] = True
            else:
                if key:
                    parsed_args[key] = arg
                    key = None
                else:
                    pass

        return parsed_args
    
    def parse_params(self, input_data):
        params = {}
        params_arr = input_data.split('&')
        for param in params_arr:
            try:
                _spl = param.split('=')
                params[_spl[0]] = _spl[1]
            except IndexError:
                pass
        
        return params
    
    def random_int(self, min, max):
        return random.randint(min, max)
    
    def parse_json(self, text):
        try:
            return json.loads(text)
        except:
            return {}
        
    def generate_temp_entity_dir(self):
        rand = self.random_int(1, 1000000) * -1
        path = Path(f'{consts['cwd']}\\storage\\collections\\{rand}')
        path.mkdir(exist_ok=True)

        return str(path)
    
    def str_to_path(self, path):
        return Path(path)
        
    def rmdir(self, str_path):
        path = Path(str_path)

        for sub in path.iterdir():
            if sub.is_dir():
                self.rmdir(sub)
            else:
                sub.unlink()

        path.rmdir()

    def find_owner(self, id, profiles, groups):
        search_array = profiles
        if id < 0:
            search_array = groups
        
        for item in search_array:
            if item.get('id') == abs(int(id)):
                return item
            
        return None

utils = Utils()
