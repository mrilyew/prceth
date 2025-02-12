from resources.Globals import platform, os

consts = {}

#def __get_storage_dir():
    #from resources.globals import config
    #return config.get("storage.path").replace("?cwd?", os.getcwd())

consts['context'] = 'cli'
consts['os_name'] = platform.system()
consts['pc_name'] = os.getenv('COMPUTERNAME', 'NoName-PC')
consts['pc_user'] = os.getlogin()
consts['pc_fullname'] = consts['pc_name'] + ', ' + consts['pc_user']
consts['cwd'] = os.getcwd()
consts["executable"] = os.path.join(consts["cwd"], "executables")
#consts['storage'] = __get_storage_dir()
#consts['tmp'] = __get_storage_dir() + "/tmp"
