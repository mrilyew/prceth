from core.api import api
from resources.globals import utils

args = utils.parse_args()
match args.get('act'):
    case None:
        print('"--act" not passed.')
