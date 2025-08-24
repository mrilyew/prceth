from utils.MainUtils import replace_cwd, replace_src
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase

class DbConnection:
    conf = {}

    def __resolve_str(self, i_str):
        conn_list = i_str.split(":///", 1)
        conn_type = conn_list[0]
        db = None

        match(conn_type):
            case "sqlite":
                connection_path = replace_src(replace_cwd(conn_list[1]))
                db = SqliteDatabase(connection_path)

        return db

    def attachDb(self, config, env):
        self.__setDb(self.__resolve_str(config.get("db.content.connection")))
        self.__setInstanceDb(self.__resolve_str(config.get("db.instance.connection")))

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
