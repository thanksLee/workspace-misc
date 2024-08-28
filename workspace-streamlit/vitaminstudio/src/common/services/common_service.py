from sqlalchemy.orm import sessionmaker

from core.databases.server.transaction_manager import TransactionManager
from core.loggers.logger_manager import app_logger
from core.configs.configs import base_config
from core.constants.global_enum_msg import ResultStatus, VSMessage


class CommonService:
    def __init__(self, tr_manager: TransactionManager):
        self._tr_manager: TransactionManager = tr_manager
        self._session: sessionmaker = self._tr_manager.get_session()
        self._app_logger = app_logger
        self._base_config = base_config
        self._ret_status = ResultStatus
        self._vs_msg = VSMessage
