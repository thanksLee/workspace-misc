from core.databases.server.db_connection_manager import db_manager
from core.databases.server.transaction_manager import TransactionManager
from core.sessions.session_state_manager import SessionStateManager


class CommonController:
    def __init__(self, db_url: str):
        self._session_state_manger = SessionStateManager()
        self._db_conn = db_manager.get_db_manager(db_url)
        self._session = self._db_conn.get_session_factory
        self._tr_manager = TransactionManager(self._session)
