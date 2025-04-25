from resources.Globals import platform, os

consts = {}

# Context
consts["context"] = "cli"

# OS
consts["os_name"] = platform.system()
consts["pc_name"] = os.getenv("COMPUTERNAME", "NoName-PC")
consts["pc_user"] = os.getlogin()
consts["pc_fullname"] = consts["pc_name"] + ", " + consts["pc_user"]

# Runtime
consts["cwd"] = os.getcwd()
consts["executable"] = os.path.join(consts["cwd"], "executables")

# Config
consts["config.hidden"] = 1
