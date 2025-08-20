from db.DbConnection import DbConnection
from storage.Storage import Storage
from app.Config import Config
from app.Logger import Logger
from utils.MainUtils import parse_args
import asyncio

config = Config()
env = Config(file_name="env.json",fallback=None)
storage = Storage(config)
logger = Logger(config, storage)

db_connection = DbConnection()
db_connection.attachDb(config, env)
db_connection.createTables()

class App():
    def __init__(self):
        self.argv = parse_args()
        self.loop = asyncio.get_event_loop()

    def cache_lists(self):
        from executables.acts import Act
        from executables.extractors import Extractor
        from executables.representations import Representation
        from executables.services import Service

        Act.findAll()
        Extractor.findAll()
        Representation.findAll()
        Service.findAll()

app = App()
