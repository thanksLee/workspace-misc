from sqlalchemy import text

from core.databases.server.base_db_manager import BaseDBManager, app_logger
from core.constants.global_enum import ProductInfo


class SQLiteManager(BaseDBManager):
    def __init__(self):
        super().__init__()
        self._app_logger = app_logger

    def add_application_name(self):
        pass

    def test_connection(self):
        sqlite_query = "select 1"
        result = self.get_session().execute(text(sqlite_query)).fetchall()
        self._app_logger.debug(f'SQLite test connection result: {result}')


class PostgreSQLManager(BaseDBManager):
    def __init__(self):
        super().__init__()
        self._app_logger = app_logger

    def add_application_name(self):
        sql = 'set application_name to :app_name'
        self.get_session().execute(text(sql), {'app_name': ProductInfo.NAME.value})

    def test_connection(self):
        pg_query = "select 1"
        result = self.get_session().execute(text(pg_query)).fetchall()
        self._app_logger.debug(f'PostgreSQL test connection result: {result}')


class OracleManager(BaseDBManager):
    def __init__(self):
        super().__init__()
        self._app_logger = app_logger

    def add_application_name(self):
        sql = 'call dbms_application_info.set_client_info(:app_name)'
        self.get_session().execute(text(sql), {'app_name': ProductInfo.NAME.value})

    def test_connection(self):
        sqlite_query = "select 1 from dual"
        result = self.get_session().execute(text(sqlite_query)).fetchall()
        self._app_logger.debug(f'Oracle test connection result: {result}')
