import shutil, platform
from datetime import datetime

def is_ffmpeg_installed():
    ffmpeg_exists = shutil.which("ffmpeg") is not None

    return ffmpeg_exists

def find_highest_in_dict(json, key_name = "photo_"):
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

def get_chrome_platform():
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

def rss_date_parse(date_string: str):
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
