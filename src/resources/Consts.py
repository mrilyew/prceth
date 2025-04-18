from resources.Globals import platform, os

consts = {}

consts["context"] = "cli"
consts["os_name"] = platform.system()
consts["pc_name"] = os.getenv("COMPUTERNAME", "NoName-PC")
consts["pc_user"] = os.getlogin()
consts["pc_fullname"] = consts["pc_name"] + ", " + consts["pc_user"]
consts["cwd"] = os.getcwd()
consts["executable"] = os.path.join(consts["cwd"], "executables")
consts["net.global_timeout"] = 1000
consts["logger.skip_categories"] = ["AsyncDownloadManager", "EntitySaveMechanism"]
consts["config.hidden"] = 1
