from core.constants.global_enum import ServerDB
from core.databases.local.db_managers import SQLiteManager
from core.configs.base import local_db_config


class LocalDBManager:

    def __init__(self, db_type):
        self._db_manager = self._get_db_manager(db_type)

    def _get_db_manager(self, db_type):
        if db_type == ServerDB.SQLITE.value:
            return SQLiteManager()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def create_local_db(self):
        self._db_manager.create_db()

    def local_db_conn(self):
        return self._db_manager.test_connection()


local_db_manager = LocalDBManager(local_db_config.db_type)

if __name__ == '__main__':
    local_db_manager.create_local_db()
    local_db_manager.local_db_conn()
