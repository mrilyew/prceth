import os

consts = {}

consts['context'] = 'cli'
consts['pc_name'] = os.getenv('COMPUTERNAME', 'NoName-PC')
consts['pc_user'] = os.getlogin()
consts['pc_fullname'] = consts['pc_name'] + ', ' + consts['pc_user']
consts['cwd'] = os.getcwd()
