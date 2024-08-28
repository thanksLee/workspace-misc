from typing import Union

from core.databases.server.base_db_manager import DBConfig
from core.databases.server.db_managers import SQLiteManager, PostgreSQLManager, OracleManager
from core.constants.global_enum import ServerDB


class DBConnectionManager:
    def __init__(self):
        self._db_managers = {}

    def add_db_manager(self, db_type: str, db_conn_str: str):
        config = DBConfig(database_url=db_conn_str)
        if db_type == ServerDB.SQLITE.value:
            manager = SQLiteManager(db_type, config)
        elif db_type == ServerDB.POSTGRESQL.value:
            manager = PostgreSQLManager(db_type, config)
        elif db_type == ServerDB.ORACLE.value:
            manager = OracleManager(db_type, config)
        # 다른 DB 매니저들도 추가 가능
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        manager.initialize()
        self._db_managers[db_type] = manager

    def get_db_manager(self, db_type: str) -> Union[SQLiteManager, PostgreSQLManager, OracleManager]:
        return self._db_managers.get(db_type)

    def close_all(self):
        for manager in self._db_managers.values():
            manager.close()


db_manager = DBConnectionManager()

if __name__ == '__main__':
    db_manager.add_db_manager('sqlite', 'sqlite:///./volumes/database/vitamin.db')
    db_conn = db_manager.get_db_manager('sqlite')
    db_conn.test_connection()
    db_conn.get_session()
    db_manager.close_all()
