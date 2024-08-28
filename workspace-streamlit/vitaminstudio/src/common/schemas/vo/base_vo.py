from pydantic import BaseModel
from core.loggers.logger_manager import app_logger


class BaseVO(BaseModel):
    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._app_logger = app_logger
