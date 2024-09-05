from core.databases.server.db_connection_manager import db_manager
from core.databases.server.transaction_manager import TransactionManager
from core.sessions.session_state_manager import SessionStateManager


class CommonController:
    def __init__(self, db_url: str):
        self._session_state_manger = SessionStateManager()
        self._db_conn = self.__get_db_conn(db_url)
        self._session = self._db_conn.get_session_factory
        self._tr_manager = TransactionManager(self._session)

    def __get_db_conn(self, db_url: str):
        db_conn = db_manager.get_db_manager(db_url)

        if db_conn is None:
            db_conn = self.__add_db_conn(db_url)

        return db_conn

    def __add_db_conn(self, db_url: str):
        db_type = db_url.split(':', 1)[0]

        if '+' in db_type:
            db_type = db_type.split('+', 1)[0]

        db_manager.add_db_manager(db_type, db_url)
        db_conn = db_manager.get_db_manager(db_url)

        return db_conn
