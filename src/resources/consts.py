import os

consts = {}

consts['context'] = 'cli'
consts['pc_name'] = os.getenv('COMPUTERNAME', 'NoName-PC')
consts['pc_user'] = os.getlogin()
consts['pc_fullname'] = consts['pc_name'] + ', ' + consts['pc_user']
consts['cwd'] = os.getcwd()
consts['vk.user_mini_fields'] = 'first_name_gen,first_name_acc,last_name_gen,last_name_acc,first_name_ins,last_name_ins,first_name_abl,last_name_abl,sex,image_status,photo_50,photo_100,photo_200,last_seen,online,blacklisted_by_me'
consts['vk.group_mini_fields'] = 'activity,photo_100,photo_200,photo_50,is_member,is_closed,description,members_count,is_subscribed'
consts['vk.user_group_fields'] = consts['vk.user_mini_fields'] + ',' + consts['vk.group_mini_fields']
