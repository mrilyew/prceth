from resources.Consts import consts
from utils.MainUtils import replace_cwd, replace_src

class DbConnection:
    def attachDb(self, config):
        content_database_type = config.get("db.content_db_type", "sqlite")
        instance_database_type = config.get("db.instance_db_type", "sqlite")
        db_set, instance_db_set = [None, None]

        from peewee import SqliteDatabase

        match(content_database_type):
            case "sqlite":
                database_path = replace_src(replace_cwd(config.get("db.sqlite_content_path")))
                db_set = SqliteDatabase(database_path)

        match(instance_database_type):
            case "sqlite":
                instance_database_path = replace_src(replace_cwd(config.get("db.sqlite_instance_path")))

                instance_db_set = SqliteDatabase(instance_database_path)

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
