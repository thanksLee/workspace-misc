from core.databases.server.db_connection_manager import db_manager
from core.configs.base import ServerDBConfig
from core.utilities.misc import get_database_url


class DBConnSample:
    def __init__(self):
        self._server_config = ServerDBConfig()

        self.__db_conn_str = f'{self._server_config.db_user}:{self._server_config.db_pwd}@{self._server_config.db_host}:{self._server_config.db_port}/{self._server_config.db_name}'
        self.__db_type = self._server_config.db_type
        self.__db_url = get_database_url(self.__db_type, self.__db_conn_str)

    @property
    def get_db_url(self):
        return self.__db_url

    @property
    def get_db_type(self):
        return self.__db_type


if __name__ == '__main__':

    db_conn_sample = DBConnSample()
    db_manager.add_db_manager(db_conn_sample.get_db_type, db_conn_sample.get_db_url)
    print(db_manager)
