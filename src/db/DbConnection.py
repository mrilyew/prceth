from utils.MainUtils import replace_cwd, replace_src
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase

class DbConnection:
    conf = {}

    def attachDb(self, config, env):
        __t_content_db = config.get("db.content_db.type", "sqlite")
        __t_instance_db = config.get("db.instance_db.type", "sqlite")
        db_content, db_instance = [None, None]

        conf = {
            'user': env.get('db.server_db.user'),
            'password': env.get('db.server_db.password'),
            'host': env.get('db.server_db.host'),
            'port': env.get('db.server_db.port')
        }

        match(__t_content_db):
            case "sqlite":
                database_path = replace_src(replace_cwd(config.get("db.sqlite.content_db.name")))
                db_content = SqliteDatabase(database_path)
            case "mysql" | "postgresql":
                __class = MySQLDatabase
                if __t_content_db == 'postgresql':
                    __class = PostgresqlDatabase

                assert conf.get('user') != None and conf.get('password') != None and conf.get('host') != None and conf.get('host') != None

                db_content = __class(config.get("db.server_db.content_db.name"),
                    user=conf.get('user'),
                    password=conf.get('password'),
                    host=conf.get('host'),
                    port=conf.get('port')
                )

        match(__t_instance_db):
            case "sqlite":
                instance_database_path = replace_src(replace_cwd(config.get("db.sqlite.instance_db.name")))

                db_instance = SqliteDatabase(instance_database_path)
            case "mysql" | "postgresql":
                __class = MySQLDatabase
                if __t_instance_db == 'postgresql':
                    __class = PostgresqlDatabase

                assert conf.get('user') != None and conf.get('password') != None and conf.get('host') != None and conf.get('host') != None

                db_instance = __class(config.get("db.server_db.instance_db.name"),
                    user=conf.get('user'),
                    password=conf.get('password'),
                    host=conf.get('host'),
                    port=conf.get('port')
                )

        self.__setDb(db_content)
        self.__setInstanceDb(db_instance)

    def __setDb(self, db):
        self.db = db

    def __setInstanceDb(self, instance_db):
        self.instance_db = instance_db

    def createTables(self):
        from db.Models.Content.ContentUnit import ContentUnit
        from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
        from db.Models.Instances.Stat import Stat
        from db.Models.Content.StorageUnit import StorageUnit
        from db.Models.Instances.ServiceInstance import ServiceInstance

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

db_connection = DbConnection()
