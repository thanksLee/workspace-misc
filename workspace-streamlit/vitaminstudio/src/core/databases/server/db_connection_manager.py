from typing import Union

from core.databases.server.base_db_manager import DBConfig
from core.databases.server.db_managers import SQLiteManager, PostgreSQLManager, OracleManager
from core.constants.global_enum import ServerDB
from core.singletons.db_connection import DBConnectionStore


class DBConnectionManager:
    def __init__(self):
        # 등록된 매니저를 DBConnectionStore에서 가져옴
        self._db_store = DBConnectionStore()

    def add_db_manager(self, db_type: str, db_url: str) -> None:
        config = DBConfig(database_url=db_url)
        if db_type == ServerDB.SQLITE.value:
            _manager = SQLiteManager()
        elif db_type == ServerDB.POSTGRESQL.value:
            _manager = PostgreSQLManager()
        elif db_type == ServerDB.ORACLE.value:
            _manager = OracleManager()
        # 다른 DB 매니저들도 추가 가능
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        _tmp_manager = self._db_store.get_manager(db_url)
        if _tmp_manager is None:
            # 매니저 초기화
            _manager.initialize(db_type, config)
            _manager.add_application_name()

            # 생성된 매니저를 DBConnectionStore에 등록
            self._db_store.register_manager(db_url, _manager)
        else:
            _manager = _tmp_manager

        _manager.test_connection()

    def get_db_manager(self, db_url: str) -> Union[SQLiteManager, PostgreSQLManager, OracleManager]:
        return self._db_store.get_manager(db_url)

    def close_all(self):
        return self._db_store.close_all()


db_manager = DBConnectionManager()

if __name__ == '__main__':

    def sql_lite():
        db_type = 'sqlite'
        db_conn_url = 'sqlite:///./volumes/database/vitamin.db'

        db_manager.add_db_manager(db_type, db_conn_url)
        db_conn = db_manager.get_db_manager(db_conn_url)
        db_conn.test_connection()
        db_conn.get_session()
        db_manager.close_all()

    def postgresql():
        db_type = 'postgresql'
        db_conn_url = 'postgresql+psycopg2://example:example@localhost:5432/example_db'

        db_manager.add_db_manager(db_type, db_conn_url)
        db_conn = db_manager.get_db_manager(db_conn_url)
        db_conn.test_connection()
        db_conn.get_session()
        db_manager.close_all()

    postgresql()
