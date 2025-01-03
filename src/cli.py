from core.api import api
from resources.globals import utils

args = utils.parse_args()
match args.get('act'):
    case None:
        print('"--act" not passed.')
    case "config.get":
        if 'param' in args:
            print(api.getOption(args['param']))
        else:
            print('\'--param\' not passed.')
    case "config.set":
        if 'param' in args and 'value' in args:
            api.setOption(args.get('param'), args['value'])
        else:
            print('\'--param\' and \'--value\' are not passed.')
    case "config.reset":
        api.resetOptions()
    case "config.all":
        options = api.getAllOptions()
        for option in options:
            print("|" + option + "|" + options[option] + "|")
