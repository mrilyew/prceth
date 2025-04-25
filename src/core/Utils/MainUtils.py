from resources.Globals import contextmanager, secrets, os, urlparse, platform, sys, random, json, consts, Path, requests, mimetypes, wget, zipfile
from collections import defaultdict
import re

class MainUtils():
    def parse_args(self):
        '''
        Parses sys.argv to array.
        '''
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
        '''
        Parses url params.
        '''
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
        '''
        Makes random integer.

        Params: min, max
        '''
        return random.randint(min, max)
    
    def parse_json(self, text):
        try:
            return json.loads(text)
        except:
            return {}
        
    def dump_json(self, text):
        try:
            return json.dumps(text)
        except:
            return {}
    
    def remove_protocol(self, strr):
        return strr.replace("https://", "").replace("http://", "").replace("ftp://", "")

    def find_owner(self, id, profiles, groups):
        '''
        Gets owner by id from "profiles" and "groups" arrays.
        '''
        search_array = profiles
        if id < 0:
            search_array = groups
        
        for item in search_array:
            if item.get('id') == abs(int(id)):
                return item
            
        return None

    # УГАДАЙ ОТКУДА :)
    def proc_strtr(self, text: str, length: int = 0, multipoint: bool = True):
        '''
        Cuts string to "length"
        '''
        newString = text[:length]

        if multipoint == False:
            return newString
        
        return newString + ("..." if text != newString else "")

    def parse_entity(self, input_string: str, allowed_entities = ["entity", "collection"]):
        '''
        Recieves entities and collections by string
        '''
        from db.Entity import Entity
        from db.Collection import Collection

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
        
        if True:
            return ''.join(filter(None, result))
        
        return ' '.join(filter(None, result))
    
    def get_mime_type(self, filename: str):
        mime_type, _ = mimetypes.guess_type(filename)
        return mime_type
    
    def get_ext(self, filename: str):
        file_splitted_array = filename.split('.')
        file_output_ext = ''
        if len(file_splitted_array) > 1:
            file_output_ext = file_splitted_array[-1]

        return file_output_ext
    
    def is_generated_ext(self, ext: str):
        return ext in ["php", "html"]
    
    def getChromishPlatform(self):
        arch = ""
        system_arch = ""
        system = platform.system().lower()
        architecture = platform.machine().lower() 

        if architecture in ['x86_64', 'amd64']:
            arch = '64'
        elif architecture in ['i386', 'i686', 'x86']:
            arch = '32'
        elif architecture in ['arm64', 'aarch64']:
            arch = 'arm64'
        else:
            arch = architecture

        match system:
            case "darwin":
                if architecture in ['arm64', 'aarch64']:
                    architecture = "arm64"
                else:
                    architecture = "x64"
                
                system_arch = f"mac-{architecture}"
            case "windows":
                system_arch = f"win{arch}"
            case _:
                system_arch = f"{system}{arch}"
        
        return system_arch
    
    def getRandomHash(self, __bytes: int = 32):
        return secrets.token_urlsafe(__bytes)
    
    def typicalPluginsList(self, folder: str):
        dir = f"{consts.get('executable')}\\{folder}"

        return Path(dir).rglob('*.py')
    
    def getExecutableList(self, folder: str = "extractors"):
        __exit = []
        __base_path = Path(f"{consts.get('executable')}\\{folder}")
        __plugins = Path(__base_path).rglob('*.py')
        for plugin in __plugins:
            if plugin.name == '__init__.py' or plugin.name == '__pycache__' or plugin.name == "Base.py":
                continue

            relative_path = plugin.relative_to(__base_path)
            module_name = str(relative_path.with_suffix("")).replace("\\", ".").replace("/", ".")
            if plugin.name.endswith('.py'):
                __exit.append(module_name)
        
        return __exit
    
    def clearJson(self, __json):
        if isinstance(__json, dict):
            return {key: self.clearJson(value) for key, value in __json.items() if isinstance(value, (dict, list, str))}
        elif isinstance(__json, list):
            return [self.clearJson(item) for item in __json if isinstance(item, (dict, list, str))]
        elif isinstance(__json, str):
            if __json.startswith("https://") == False and __json.startswith("http://") == False:
                return __json
        elif isinstance(__json, int):
            return __json
        else:
            return None
        
    def nameFromURL(self, input_url):
        parsed_url = urlparse(input_url)
        path = parsed_url.path

        if path.endswith('/') or path == "":
            return "index", "html"
        
        filename = os.path.basename(path)
        OUTPUT_NAME, OUTPUT_NAME_EXT = os.path.splitext(filename)
        if not OUTPUT_NAME_EXT:
            OUTPUT_NAME_EXT = ""
        else:
            OUTPUT_NAME_EXT = OUTPUT_NAME_EXT[1:]
        
        return OUTPUT_NAME, OUTPUT_NAME_EXT
    
    @contextmanager
    def overrideDb(self, __class, __db):
        old_db = __class._meta.database
        __class._meta.database = __db
        yield
        __class._meta.database = old_db
    
    def validName(self, text):
        '''
        Creates saveable name (removes forbidden in NTFS characters)
        '''
        safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', text)
        safe_filename = re.sub(r'_+', '_', safe_filename)
        safe_filename = safe_filename.strip('_')
        if not safe_filename:
            return "unnamed"
        
        return safe_filename

    def replaceStringsInDict(self, input_data, link_to_linked_files, recurse_level = 0):
        if isinstance(input_data, dict):
            return {key: self.replaceStringsInDict(value, link_to_linked_files) for key, value in input_data.items()}
        elif isinstance(input_data, list):
            return [self.replaceStringsInDict(item, link_to_linked_files) for item in input_data]
        elif isinstance(input_data, str):
            try:
                if "__lcms|entity_" in input_data:
                    got_id = int(input_data.replace("__lcms|entity_", ""))
                    for linked in link_to_linked_files:
                        if linked.id == got_id and linked.self_name == "entity":
                            return linked.getFormattedInfo(recursive=True,recurse_level=recurse_level+1)
                        else:
                            return input_data
                elif "__lcms|file_" in input_data:
                    got_id = int(input_data.replace("__lcms|file_", ""))
                    for linked in link_to_linked_files:
                        if linked.id == got_id and linked.self_name == "file":
                            return linked.getFormattedInfo(recursive=True,recurse_level=recurse_level+1)
                        else:
                            return input_data
                else:
                    return input_data
            except Exception as __e:
                return input_data
        else:
            return input_data

    def findHighestInDict(self, json, key_name = "photo_"):
        max_size = -1
        for key in json:
            try:
                if key != None and key.startswith(key_name):
                    cur = int(key.replace(key_name, ""))
                    if cur > max_size:
                        max_size = cur
            except:
                continue
    
        return max_size
        
utils = MainUtils()
