import secrets, os, sys, random, json, mimetypes
from resources.Descriptions import descriptions
from contextlib import contextmanager
from resources.Consts import consts
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import urlencode
import re

def parse_args():
    '''
    Parses sys.argv to dict.
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

def parse_params(input_data):
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

def random_int(min, max):
    '''
    Makes random integer.

    Params: min, max
    '''
    return random.randint(min, max)

def parse_json(text):
    '''
    Parses JSON from text
    '''
    return json.loads(text)

def dump_json(obj, indent=None):
    '''
    Serializes JSON object to text
    '''
    return json.dumps(obj,ensure_ascii=False,indent=indent)

def remove_protocol(link):
    '''
    Removes protocol from link.
    '''
    protocols = ["https", "http", "ftp"]
    final_link = link
    for protocol in protocols:
        if final_link.startswith(protocol):
            final_link.replace(f"{protocol}://", "")

    return final_link

# откуда-то взято
def proc_strtr(text: str, length: int = 100, multipoint: bool = True):
    '''
    Cuts string to "length".
    '''
    newString = text[:length]

    if multipoint == False:
        return newString

    return newString + ("..." if text != newString else "")

def extract_metadata_to_dict(mtdd):
    metadata_dict = defaultdict(list)

    for line in mtdd:
        key_value = line.split(": ", 1)
        if key_value[0].startswith('- '):
            key = key_value[0][2:]
            metadata_dict[key].append(key_value[1])

    return dict(metadata_dict)

def json_values_to_string(data, separator = ''):
    result = []

    if isinstance(data, dict):
        for value in data.values():
            result.append(json_values_to_string(value))

    elif isinstance(data, list):
        for item in data:
            result.append(json_values_to_string(item))

    else:
        return str(data)

    return separator.join(filter(None, result))

def get_mime_type(filename: str):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type

def get_ext(filename: str):
    file_splitted_array = filename.split('.')
    file_output_ext = ''
    if len(file_splitted_array) > 1:
        file_output_ext = file_splitted_array[-1]

    return file_output_ext

def get_random_hash(__bytes: int = 32):
    return secrets.token_urlsafe(__bytes)

def clear_json(__json):
    if isinstance(__json, dict):
        return {key: clear_json(value) for key, value in __json.items() if isinstance(value, (dict, list, str))}
    elif isinstance(__json, list):
        return [clear_json(item) for item in __json if isinstance(item, (dict, list, str))]
    elif isinstance(__json, str):
        if __json.startswith("https://") == False and __json.startswith("http://") == False:
            return __json
    elif isinstance(__json, int):
        return __json
    else:
        return None

def name_from_url(input_url):
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
def override_db(__classes = [], __db = None):
    '''
    Overrides db for a time
    '''
    old_db = None
    for __class in __classes:
        old_db = __class._meta.database
        __class._meta.database = __db
    
    yield

    for __class in __classes:
        __class._meta.database = old_db

def valid_name(text):
    '''
    Creates saveable name (removes forbidden characters in NTFS)
    '''
    safe_filename = re.sub(r'[\\/*?:"<>| ]', '_', text)
    safe_filename = re.sub(r'_+', '_', safe_filename)
    safe_filename = safe_filename.strip('_')
    if not safe_filename:
        return "unnamed"

    return safe_filename

def replace_cwd(input_string: str):
    return input_string.replace("?cwd?", str(consts.get("cwd")))

def replace_src(input_string: str):
    return input_string.replace("\\src", "")

def list_conversation(i_list):
    if type(i_list) == dict:
        return [i_list]

    return i_list

def resolve_lang(translation_dict: dict, lang_code: str):
    if translation_dict == None:
        return None

    return translation_dict.get(lang_code, translation_dict.get("eng"))

def resolve_doc(i):
    __lang_code = consts.get('ui.lang', 'eng')

    out = i
    if type(i) == str:
        out = descriptions.get(i)

    return resolve_lang(out, __lang_code)

def is_valid_json(i):
    try:
        val = json.loads(i)

        return val != None and type(val) != int and type(val) != str
    except json.JSONDecodeError:
        return False
    except TypeError:
        return False
