import sys
import random
import json

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
            elif arg.startswith('-'):
                if key:
                    parsed_args[key] = True
                key = arg[1:]
                parsed_args[key] = True
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

utils = Utils()
