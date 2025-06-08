from resources.Consts import consts
from utils.MainUtils import replace_cwd, replace_src
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, OperationalError

class DbConnection:
    def attachDb(self, config):
        content_database_type = config.get("db.content_db.type", "sqlite")
        instance_database_type = config.get("db.instance_db.type", "sqlite")
        db_set, instance_db_set = [None, None]


        __server_db_user = config.get('db.server_db.user')
        __server_db_pass = config.get('db.server_db.password')
        __server_db_host = config.get('db.server_db.host')
        __server_db_port = config.get('db.server_db.port')

        match(content_database_type):
            case "sqlite":
                database_path = replace_src(replace_cwd(config.get("db.sqlite.content_db.name")))
                db_set = SqliteDatabase(database_path)
            case "mysql" | "postgresql":
                __class = MySQLDatabase
                if content_database_type == 'postgresql':
                    __class = PostgresqlDatabase

                assert __server_db_user != None and __server_db_pass != None and __server_db_host != None and __server_db_port != None
                
                db_set = __class(config.get("db.server_db.content_db.name"),
                    user=__server_db_user,
                    password=__server_db_pass,
                    host=__server_db_host,
                    port=__server_db_port
                )

        match(instance_database_type):
            case "sqlite":
                instance_database_path = replace_src(replace_cwd(config.get("db.sqlite.instance_db.name")))

                instance_db_set = SqliteDatabase(instance_database_path)
            case "mysql" | "postgresql":
                __class = MySQLDatabase
                if instance_database_type == 'postgresql':
                    __class = PostgresqlDatabase

                assert __server_db_user != None and __server_db_pass != None and __server_db_host != None and __server_db_port != None

                instance_db_set = __class(config.get("db.server_db.instance_db.name"),
                    user=__server_db_user,
                    password=__server_db_pass,
                    host=__server_db_host,
                    port=__server_db_port
                )

        self.__setDb(db_set)
        self.__setInstanceDb(instance_db_set)

    def __setDb(self, db):
        self.db = db

    def __setInstanceDb(self, instance_db):
        self.instance_db = instance_db

    def createTables(self):
        from db.ContentUnit import ContentUnit
        from db.ContentUnitRelation import ContentUnitRelation
        from db.Stat import Stat
        from db.StorageUnit import StorageUnit
        from db.ServiceInstance import ServiceInstance

        tables_list = [ContentUnitRelation, ContentUnit, StorageUnit]
        tables_list_app = [Stat, ServiceInstance]

        # Appending content db
        self.db.bind(tables_list)

        self.db.connect()
        self.db.create_tables(tables_list, safe=True)
        self.db.close()

        # Appending instance db
        self.instance_db.bind(tables_list_app)

        self.instance_db.connect()
        self.instance_db.create_tables(tables_list_app, safe=True)
        self.instance_db.close()
