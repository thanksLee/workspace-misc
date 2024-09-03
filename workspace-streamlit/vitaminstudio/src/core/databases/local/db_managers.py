import os
from core.databases.local.base_db_manager import BaseDatabaseManager
from core.configs.configs import local_db_config
from core.utilities.misc import get_database_url


class SQLiteManager(BaseDatabaseManager):
    def __init__(self):
        super().__init__()

        self._db_type = local_db_config.db_type
        self._db_path = f'{local_db_config.db_path}/{local_db_config.db_name}'
        self._database_url = get_database_url(self._db_type, self._db_path)

    def create_db(self):
        if not os.path.exists(self._db_path):
            open(self._db_path, 'a').close()
            self._app_logger.info("SQLite database created successfully!")
        else:
            self._app_logger.warning("SQLite database already exists.")

    def test_connection(self):
        from core.databases.server.db_connection_manager import db_manager

        db_manager.add_db_manager(self._db_type, self._database_url)
        db_conn = db_manager.get_db_manager(self._database_url)
        db_conn.test_connection()
