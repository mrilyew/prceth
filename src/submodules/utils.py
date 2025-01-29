from resources.globals import os, sys, random, json, consts, Path, requests, mimetypes, wget, zipfile
from collections import defaultdict

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

    def find_owner(self, id, profiles, groups):
        search_array = profiles
        if id < 0:
            search_array = groups
        
        for item in search_array:
            if item.get('id') == abs(int(id)):
                return item
            
        return None
    
    def fast_get_request(self, url='', user_agent=''):
        result = requests.get(url, headers={
            'User-Agent': user_agent
        })
        parsed_result = None
        if result.headers.get('content-type').index('application/json') != -1:
            parsed_result = json.loads(result.content)

        return parsed_result
    
    def proc_strtr(self, text, length = 0):
        newString = text[:length]

        return newString + ("..." if text != newString else "")
    
    def parse_entity(self, input_string, allowed_entities = ["entity", "collection"]):
        from db.entity import Entity
        from db.collection import Collection

        elements = input_string.split('entity')
        if len(elements) > 1 and elements[0] == "":
            if "entity" in allowed_entities:
                entity_id = elements[1]
                return Entity.get(entity_id)
        elif 'collection' in input_string:
            if "collection" in allowed_entities:
                collection_id = input_string.split('collection')[1]
                return Collection.get(collection_id)
        else:
            return None

    def extract_metadata_to_dict(self, mtdd):
        metadata_dict = defaultdict(list)

        for line in mtdd:
            key_value = line.split(": ", 1)
            if key_value[0].startswith('- '):
                key = key_value[0][2:]
                metadata_dict[key].append(key_value[1])

        return dict(metadata_dict)
    
    def json_values_to_string(self, data):
        result = []

        if isinstance(data, dict):
            for value in data.values():
                result.append(self.json_values_to_string(value))

        elif isinstance(data, list):
            for item in data:
                result.append(self.json_values_to_string(item))

        else:
            return str(data)
        
        return ' '.join(filter(None, result))
    
    def get_mime_type(self, filename):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type
    
    def get_ext(self, filename):
        file_splitted_array = filename.split('.')
        file_output_ext = ''
        if len(file_splitted_array) > 1:
            file_output_ext = file_splitted_array[-1]

        return file_output_ext
    
    def is_generated_ext(self, ext):
        return ext in ["php", "html"]
    
    def download_chrome_driver(self, endpoint = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"):
        #current_version_response = requests.get(endpoint)
        #version_number = current_version_response.text

        #download_url  = "https://chromedriver.storage.googleapis.com/" + version_number +"/chromedriver_win32.zip"
        # TODO: Add support for another platforms
        download_url  = "https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.110/win64/chromedriver-win64.zip"
        download_path = consts["tmp"] + '/chrome/chromedriver.zip'
        latest_driver_zip = wget.download(download_url, download_path)
        with zipfile.ZipFile(latest_driver_zip, 'r') as zip_ref:
            zip_ref.extractall(consts["tmp"] + "/chrome")

        os.remove(latest_driver_zip)

        return consts["tmp"] + "/chrome/chromedriver.exe"

utils = Utils()
