from typing import Dict, Union

from core.databases.server.base_db_manager import BaseDBManager
from core.loggers.logger_manager import app_logger, LoggerType
from .singleton_meta import SingletonMeta


class DBConnectionStore(metaclass=SingletonMeta):
    """
    DB 연결 객체를 중앙에서 관리하는 싱글톤 클래스
    """
    _db_managers: Dict[str, 'BaseDBManager']  # 타입 힌트 추가
    _app_logger: LoggerType

    def __new__(cls, *args, **kwargs):
        # 싱글톤 인스턴스가 존재하지 않으면 생성
        if not hasattr(cls, '_instance'):
            cls._instance = super(DBConnectionStore, cls).__new__(cls)
            cls._instance._db_managers = {}  # 초기화 작업을 여기서 수행
            cls._instance._app_logger = app_logger
        return cls._instance

    def register_manager(self, db_conn_str: str, manager: BaseDBManager):
        if db_conn_str not in self._db_managers:
            self._db_managers[db_conn_str] = manager
        else:
            self._app_logger.info(f"Manager for {db_conn_str} already exists.")

        self._app_logger.debug(f'self._db_managers[db_conn_str] : {self._db_managers[db_conn_str]}')

    def get_manager(self, db_conn_str: str) -> Union[BaseDBManager, None]:
        self._app_logger.debug(f'db_conn_str - {db_conn_str} : {self._db_managers.get(db_conn_str)}')
        return self._db_managers.get(db_conn_str)

    def close_all(self):
        for manager in self._db_managers.values():
            manager.close()
        self._db_managers.clear()
