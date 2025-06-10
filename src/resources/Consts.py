from pathlib import Path
import platform, os

consts = {}

# Context
consts["context"] = "cli"

# OS
consts["os_name"] = platform.system()
consts["pc_name"] = os.getenv("COMPUTERNAME", "NoName-PC")
consts["pc_user"] = os.getlogin()
consts["pc_fullname"] = consts["pc_name"] + ", " + consts["pc_user"]

# Runtime
consts["cwd"] = Path(os.getcwd())
consts["executables"] = Path(os.path.join(consts.get('cwd'), "executables"))
consts["representations"] = Path(os.path.join(consts.get('cwd'), "representations"))

# Config
consts["config.hidden"] = 1
